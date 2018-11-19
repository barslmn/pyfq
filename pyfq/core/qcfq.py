
from pyfq.utils.fastq import Fastq
from collections import Counter

import os
import sys
from importlib import util

mpl_exists = util.find_spec('matplotlib') is not None
scipy_exists = util.find_spec('scipy') is not None
numpy_exists = util.find_spec('numpy') is not None

if mpl_exists and scipy_exists and numpy_exists:
    import matplotlib.pyplot as plt
    from scipy import stats
    import numpy as np
else:
    sys.stdout.write('Matplotlib, Scipy and Numpy are required.')


class FastqQualityCheck(Fastq):

    """Docstring for FastqQualityCheck. """

    def __init__(self, fastq_file, output_file=None):
        super().__init__(fastq_file)

        self.output_file = output_file
        self.img_dir = self.output_file.split('.')[0]

    def translatephredscores_2_p(self):
        new_fastq = {}
        for identifier, read, phred_scores in self:
            new_fastq[identifier] = [
                read, [10**-((ord(phred_score) - 33) / 10) for phred_score in phred_scores]]
        self.fastq = new_fastq

    def translatephredscores_2_q(self):
        new_fastq = {}
        for identifier, read, phred_scores in self:
            new_fastq[identifier] = [
                read, [ord(phred_score) - 33 for phred_score in phred_scores]]
        self.fastq = new_fastq

    def per_base_sequence_quality(self):
        self.fig_name = 'per_base_sequence_quality'
        fig, ax = plt.subplots()
        ax.boxplot(
            list(map(list, zip(*[read_record[2] for read_record in self]))), 0, '')
        ax.set_title('Average Quality Scores per Base')
        ax.set_xlabel('Base Position')
        ax.set_ylabel('Average Quality Scores')
        return fig

    def per_sequence_quality_scores(self):
        self.fig_name = 'per_sequence_quality_scores'
        fig, ax = plt.subplots()
        average_qualities = [stats.describe(read_record[2]).mean
                             for read_record in self]
        average_qualities.sort()
        ax.plot(average_qualities)
        ax.set_title('Average Quality Scores per Read')
        ax.set_xlabel('Reads')
        ax.set_ylabel('Average Quality Scores')
        return fig

    def per_sequence_gc_content(self):
        self.fig_name = 'per_sequence_gc_content'
        # Make this a distribution
        # Scipy
        fig, ax = plt.subplots(1, 1)
        average_gc_content = [(Counter(read_record[1])['G'] + Counter(read_record[1])[
                               'C']) / len(read_record[1]) * 100 for read_record in self]

        ax.hist(average_gc_content, density=True)

        xt = plt.xticks()[0]
        xmin, xmax = min(xt), max(xt)
        x = np.linspace(xmin, xmax, len(average_gc_content))

        # get mean and standard deviation
        m, s = stats.norm.fit(average_gc_content)
        ax.plot(x, stats.norm.pdf(x, m, s), label='norm pdf')

        ax.set_title('GC content per Read')
        ax.set_xlabel('Mean GC content(%)')
        ax.set_ylabel('Reads')
        return fig

    def sequence_length_distribution(self):
        self.fig_name = 'sequence_length_distribution'
        fig, ax = plt.subplots()
        sequence_lengths = [len(read_record[1]) for read_record in self]

        ax.hist(sequence_lengths, density=True)

        xt = plt.xticks()[0]
        xmin, xmax = min(xt), max(xt)
        x = np.linspace(xmin, xmax, len(sequence_lengths))

        # get mean and standard deviation
        m, s = stats.norm.fit(sequence_lengths)
        ax.plot(x, stats.norm.pdf(x, m, s), label='norm pdf')

        ax.set_title('Sequence Length Distribution')
        ax.set_xlabel('Sequence Length')
        ax.set_ylabel('Reads')
        return fig

    def create_plots(self):
        self.figs_dict = {}
        self.translatephredscores_2_q()

        plot_functions = [self.per_base_sequence_quality,
                          #self.per_sequence_quality_scores,
                          self.per_sequence_gc_content,
                          self.sequence_length_distribution,
                          ]

        for plot_function in plot_functions:
            fig = plot_function()
            fig_path = os.path.join(
                self.img_dir, '{}.png'.format(self.fig_name))
            fig.savefig(fig_path)
            self.figs_dict[self.fig_name] = fig_path

    def create_html_report(self):
        if not os.path.exists(self.img_dir):
            os.mkdir(self.img_dir)

        self.create_plots()
        with open(self.output_file, 'w') as f:
            # Create TOC
            f.write('<html>\n</body>\n<div id="TOC">\n<ul>\n')
            for fig_name in self.figs_dict:
                f.write('<li><a href="#{0}">{0}</a></li>\n'.format(fig_name))
            f.write('</ul>\n</div>\n')
            # Create images
            for fig_name, fig_path in self.figs_dict.items():
                f.write(
                    '<div id="{0}"><img src="{1}" alt = "{0}"></div>\n'.format(fig_name, fig_path))
            f.write('</body>\n</html>')


def main(args):
    my_fastq_file = args.input
    my_output_file = args.output
    my_output_format = args.output_format

    my_fqc = FastqQualityCheck(my_fastq_file, my_output_file)

    if my_output_format == 'html':
        my_fqc.create_html_report()

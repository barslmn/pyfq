import matplotlib.pyplot as plt

import os

# Comment out this before building
#from pyfq.utils.fastq import Fastq
# Remove this part after dev
import sys
sys.path.append(os.path.abspath('..'))
from utils.fastq import Fastq


class FastqQualityCheck(Fastq):

    """Docstring for FastqQualityCheck. """

    def __init__(self, fastq_file):
        super().__init__(fastq_file)

    def translatephredscores(self):
        new_fastq = {}
        for identifier, read, phred_scores in self:
            new_fastq[identifier] = [read, [10**-((ord(phred_score) - 33) / 10) for phred_score in phred_scores]]
        self.fastq = new_fastq

    def drawboxplot(self):
        plt.boxplot(list(map(list, zip(*[read_record[2] for read_record in self]))), 0, '')
        plt.show()



def main():
    """TODO: Docstring for main.
    :returns: TODO

    """
    pass

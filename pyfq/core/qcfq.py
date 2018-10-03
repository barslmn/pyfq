import matplotlib.pyplot as plt


class FastqQualityCheck():

    """Docstring for FastqQualityCheck. """

    def __init__(self, fastqfile):
        self.fastqfile = fastqfile

    def __str__(self):
        s = ''
        for read in self.readfastqfile:
            s += read[1]
        return s

    def __len__(self):
        readlengths = [str(len(read[1])) for read in self.readfastqfile]
        return set(readlengths)

    def chunks(self, l, n):
        '''Yield successive n-size chunks from l.'''
        for i in range(0, len(l), n):
            yield l[i:i + n]

    @property
    def readfastqfile(self):
        with open(self.fastqfile, 'r') as f:
            reads = f.read()
            f.close()
        groups = reads.split('\n')[:-1]
        read_groups = [chunk for chunk in self.chunks(groups, 4)]
        return read_groups

    def translatephredscores(self):
        self.p_errors = []
        for read in self.readfastqfile:
            self.p_errors.append([10**-((ord(phredscore) - 33) / 10)
                                  for phredscore in read[3]])
        return self.p_errors

    def convert2fasta(self):
        fastareads = [reads[:2] for reads in self.readfastqfile]
        fastareads = '\n'.join(
            [reads[0].replace('@', '>', 1) + '\n' + reads[1] for reads in fastareads])
        return fastareads

    def writefasta(self, fastafile, fastareads):
        with open(fastafile, 'w') as f:
            f.write(fastareads)
            f.close()

    def drawboxplot(self, p_errors):
        plt.boxplot(list(map(list, zip(*p_errors))), 0, '')
        plt.show()

def main():
    """TODO: Docstring for main.
    :returns: TODO

    """
    pass

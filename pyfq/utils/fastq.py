
class Fastq(object):

    def __init__(self, fastq_file):
        self.fastq_file = fastq_file

    def __str__(self):
        return ''

    def __repr__(self):
        return ''

    def __len__(self):
        '''Returns number of reads
        '''
        return  len(self.read_records)

    def chunks(self, l, n):
        '''Yield successive n-size chunks from l.'''
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def read_fastq(self):
        with open(self.fastq_file, 'r') as f:
            contents = f.read()
            f.close()
        all_reads = contents.split('\n')[:-1]
        self.read_records = {chunk[0]:[chunk[1], chunk[3]] for chunk in self.chunks(all_reads, 4)}
        yield self.read_records

a = ParseFastq('/home/bar/Workbench/pybench/pyfqc/SP1.fq')
a.read_fastq()
len(a)
for i in a.read_fastq:
    print(i)

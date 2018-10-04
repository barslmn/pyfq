import os
import sys
import gzip


class Fastq():

    def __init__(self, fastq_file):
        self.fastq_file = fastq_file
        self.read_fastq()

    def __str__(self):
        return 'Fastq object for {}'.format(os.path.basename(self.fastq_file))

    def __repr__(self):
        return 'Fastq object for {}'.format(os.path.basename(self.fastq_file))

    def __len__(self):
        '''Returns number of reads'''
        return len(self.fastq)

    def __iter__(self):
        for k, v in self.fastq.items():
            yield k, v[0], v[1]

    def chunks(self, l, n):
        '''Yield successive n-size chunks from l.'''
        for i in range(0, len(l), n):
            yield l[i:i + n]

    @property
    def fastq(self):
        return self.read_records

    @fastq.setter
    def fastq(self, new_records):
        self.read_records = new_records
        

    def read_fastq(self):
        self.read_records = {}
        if self.fastq_file.endswith(('.fastq.gz', 'fq.gz')):
            with gzip.open(self.fastq_file, 'rb') as f:
                for fastq_record in self.chunks(f.read().splitlines(), 4):
                    fastq_record = [line.decode('utf-8')
                                    for line in fastq_record]
                    self.read_records[fastq_record[0]] = [
                        fastq_record[1], fastq_record[3]]
        elif self.fastq_file.endswith(('.fastq', '.fq')):
            with open(self.fastq_file, 'r') as f:
                for fastq_record in self.chunks(f.read().splitlines(), 4):
                    self.read_records[fastq_record[0]] = [
                        fastq_record[1], fastq_record[3]]
        else:
            sys.stderr.write('Are you sure this is a fastq file??\n')
            sys.exit()
        self.read_records

    def write_fastq(self, fastq_file):
        with open(fastq_file, 'w') as f:
            for read_record in self:
                f.write('{}\n{}\n+\n{}\n'.format(
                    read_record[0], read_record[1], read_record[2]))
        pass

    def write_fasta(self, fasta_file):
        with open(fasta_file, 'w') as f:
            for read_record in self:
                f.write('>{}\n{}\n'.format(
                    read_record[0].strip('@'), read_record[1]))
            f.close()

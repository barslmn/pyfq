#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'bars'

import os
import shutil
import argparse


def main(args):
    inputdir = args.input
    if args.output == None:
        outputdir = 'cats/'
    else:
        outputdir == args.output

    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    fastqncs = [fastq for fastq in os.listdir(
        inputdir) if fastq.endswith('fastq')]
    fastqgzs = [fastq for fastq in os.listdir(
        inputdir) if fastq.endswith('fastq.gz')]
    if len(fastqncs) > len(fastqgzs):
        outputtype = ''
        fastqs = fastqncs
    else:
        outputtype = '.gz'
        fastqs = fastqgzs

    samples = set([fastq.split('_')[0] for fastq in fastqs])

    samplefastqs_f = {sample: [
        fastq for fastq in fastqs if sample in fastq and 'R1' in fastq] for sample in samples}

    samplefastqs_r = {sample: [
        fastq for fastq in fastqs if sample in fastq and 'R2' in fastq] for sample in samples}

    for sample, fastqs in samplefastqs_f.items():
        with open(outputdir + sample + '_S_R1.fastq' + outputtype, 'wb') as wfp:
            for fastq in sorted(fastqs):
                with open(fastq, 'rb') as rfp:
                    shutil.copyfileobj(rfp, wfp)

    for sample, fastqs in samplefastqs_r.items():
        with open(outputdir + sample + '_S_R2.fastq' + outputtype, 'wb') as wfp:
            for fastq in sorted(fastqs):
                with open(fastq, 'rb') as rfp:
                    shutil.copyfileobj(rfp, wfp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=False,
                        default='./', type=str,
                        help='Directory of fastq(.gz)s to cat')
    parser.add_argument('-o', '--output', required=False,
                        default=None, type=str,
                        help='Directory to write catted fastq(.gz)(s)')
    args = parser.parse_args()
    main(args)

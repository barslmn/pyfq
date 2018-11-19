#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'bars'

import os
import shutil


def main(args):
    input_dir = args.input
    if args.output is not None:
        output_dir = args.output
    else:
        output_dir = 'cats/'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    fastqncs = [fastq for fastq in os.listdir(
        input_dir) if fastq.endswith(('fastq', 'fq'))]
    fastqgzs = [fastq for fastq in os.listdir(
        input_dir) if fastq.endswith(('fastq.gz', 'fq.gz'))]
    if len(fastqncs) > len(fastqgzs):
        outputtype = ''
        fastqs = fastqncs
    else:
        outputtype = '.gz'
        fastqs = fastqgzs

    samples = set(['_'.join(fastq.split('_')[:2]) for fastq in fastqs])

    samplefastqs_f = {sample: [
        fastq for fastq in fastqs if sample in fastq and 'R1' in fastq] for sample in samples}

    samplefastqs_r = {sample: [
        fastq for fastq in fastqs if sample in fastq and 'R2' in fastq] for sample in samples}

    for sample, fastqs in samplefastqs_f.items():
        with open(output_dir + sample + '_R1.fastq' + outputtype, 'wb') as wfp:
            for fastq in sorted(fastqs):
                with open(fastq, 'rb') as rfp:
                    shutil.copyfileobj(rfp, wfp)

    for sample, fastqs in samplefastqs_r.items():
        with open(output_dir + sample + '_R2.fastq' + outputtype, 'wb') as wfp:
            for fastq in sorted(fastqs):
                with open(fastq, 'rb') as rfp:
                    shutil.copyfileobj(rfp, wfp)

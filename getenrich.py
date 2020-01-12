
import os
import pandas
import pybedtools
import numpy as np
import _genomic_signal


class Binner(object):
    def __init__(self, genome, windowsize, chrom=None, window_cache_dir=".",
                 npz_dir='.', metric='mean0'):

        self.chromsizes = pybedtools.chromsizes(genome)
        if chrom is None:
            self.chroms = sorted(self.chromsizes.keys())
        else:
            self.chroms = [chrom]
        self.windowsize = windowsize
        self.window_cache_dir = window_cache_dir

    def make_windows(self, chrom, force=False):
        chromsize = self.chromsizes[chrom][1]
        bed = pybedtools.BedTool(
            '{0} 0 {1}'.format(chrom, chromsize),
            from_string=True
        )
        output = os.path.join(
            self.window_cache_dir,
            '%s.%sbp_windows.bed' % (chrom, self.windowsize))
        if not os.path.exists(output) and not force:
            windows = pybedtools.BedTool()\
                .window_maker(
                    b=bed,
                    i='winnum',
                    w=self.windowsize,
                    output=output,
                )
        return output

    def to_npz(self, bigwig, metric='mean0', outdir=None):

        if isinstance(bigwig, _genomic_signal.BigWigSignal):
            bigwig = bigwig.fn

        if outdir is None:
            outdir = os.path.dirname(bigwig)

        basename = os.path.basename(bigwig)
        windowsize = self.windowsize

        outfiles = []
        for chrom in self.chroms:
            tmp_output = pybedtools.BedTool._tmp()
            windows = self.make_windows(chrom)

            outfile = os.path.join(
                outdir,
                '{basename}.{chrom}.{windowsize}.{metric}'.format(**locals())
                + '.npz')
            cmds = [
                'bigWigAverageOverBed',
                bigwig,
                windows,
                tmp_output]
            os.system(' '.join(cmds))
            names = ['name', 'size', 'covered', 'sum', 'mean0', 'mean']
            df = pandas.read_table(tmp_output, names=names)
            x = df.size.cumsum() - df.size / 2
            y = df[metric]
            np.savez(outfile, x=x, y=y)
            outfiles.append(outfile)
            del x, y, df
        return outfiles

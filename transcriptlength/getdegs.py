import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import os
from itertools import repeat

DIR = Path("/home/hanwenying")
LENGTHDIR = DIR / "rothman-anna/transcriptlength"
DATADIR = DIR / "rothman-data/anna/transcriptlength"
OUTDIR = LENGTHDIR / "out"
STRATDIR = OUTDIR / "stratified-rawcounts"
DEGDIR = OUTDIR / "deglists"

os.makedirs(DEGDIR, exist_ok=True)

metadata = pd.read_csv(OUTDIR / "metadata.tsv", sep='\t', dtype=str)
# testdf = pd.read_csv(STRATDIR / "1_0001.tsv", sep='\t')

# # print(metadata[metadata['SAMPLE'].isin(testdf.columns)])

# tpmdata1 = testdf.T[2:].reset_index()
# tpmdata1.columns = ['Name'] + list(testdf['Name'])
# tpmdata1.set_index('Name', inplace=True)
# tpmdata1 = tpmdata1.astype(int)
# metadata1 = metadata[metadata['SAMPLE'].isin(testdf.columns)]
# metadata1.set_index('SAMPLE', inplace=True)

# dds = DeseqDataSet(counts=tpmdata1, metadata=metadata1, design_factors='AGE', refit_cooks=True)
# dds.deseq2()
# ds = DeseqStats(dds, contrast=['AGE', '40-49', '20-29'])
# ds.summary()
# deg = ds.results_df.copy()

# print(deg)

def getdeg(metadata: pd.DataFrame, strat: str, stratdir: Path, outdir: Path) -> None:
	rawcounts = pd.read_csv(stratdir / f"{strat}.tsv", sep='\t', dtype=str)
	genes = list(rawcounts['Name'])
	samples = rawcounts.columns
	rawcounts = rawcounts.T[2:].reset_index()
	rawcounts.columns = ['Name'] + genes
	rawcounts.set_index('Name', inplace=True)
	rawcounts = rawcounts.astype(int)

	metadata = metadata[metadata['SAMPLE'].isin(samples)]
	metadata.set_index('SAMPLE', inplace=True)

	rawcounts = rawcounts.loc[metadata.index]

	ages = list(metadata['AGE'].unique())
	for age in ages:
		if age != '20-29':
			print(f'\t{age}')
			dds = DeseqDataSet(counts=rawcounts, metadata=metadata, design_factors='AGE', refit_cooks=True, n_cpus=12, quiet=True)
			dds.deseq2()
			ds = DeseqStats(dds, contrast=['AGE', age, '20-29'], n_cpus=12, quiet=True)
			ds.summary()
			deg = ds.results_df.copy()

			deg.to_csv(outdir / f"{strat}_{age}.tsv", sep='\t')


if __name__ == "__main__":
	strats = [p.stem for p in STRATDIR.iterdir() if p.is_file()]
	for strat in strats:
		print(strat, flush=True)
		getdeg(metadata, strat, STRATDIR, DEGDIR)
# 	print("Starting MP", flush=True)
# 	with ProcessPoolExecutor(max_workers=12) as exec:
# 		exec.map(getdeg, repeat(metadata), strats, repeat(STRATDIR), repeat(DEGDIR))
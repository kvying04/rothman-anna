import pandas as pd
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import os

DIR = Path("/home/hanwenying")
LENGTHDIR = DIR / "rothman-anna/transcriptlength"
DATADIR = DIR / "rothman-data/anna/transcriptlength"
OUTDIR = LENGTHDIR / "out"
STRATDIR = OUTDIR / "stratified-rawcounts"

os.makedirs(STRATDIR, exist_ok=True)


rawcounts = pd.read_parquet(DATADIR / "rawcounts-gtex-v11.parquet", engine='pyarrow').reset_index()
metadata = pd.read_csv(OUTDIR / "metadata.tsv", sep='\t', dtype=str)

stratsamples = metadata.groupby(['TISSUE', 'SEX'])['SAMPLE'].apply(list)


for (tissue, sex), samplelist in stratsamples.items():
	print(tissue, sex, flush=True)
	strattpm = rawcounts[['Name', 'Description'] + samplelist]
	strattpm.to_csv(STRATDIR / f"{sex}_{tissue}.tsv", sep='\t', index=False)
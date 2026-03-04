import pandas as pd
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import os

DIR = Path("/home/hanwenying")
LENGTHDIR = DIR / "rothman-anna/transcriptlength"
DATADIR = DIR / "rothman-data/anna/transcriptlength"
OUTDIR = LENGTHDIR / "out"


rawcounts = pd.read_parquet(DATADIR / "rawcounts-gtex-v11.parquet", engine='pyarrow').reset_index()
print(rawcounts.head())

metadata = pd.read_csv(DATADIR / "subjectmetadata-gtex-v11.txt", sep='\t')
metadata.drop(columns=['DTHHRDY'], inplace=True)

samplemetadata = pd.DataFrame()

samplecol = rawcounts.columns[2:]
subjcol = samplecol.str.split('-').str[:2].str.join('-')
tissuecol = samplecol.str.split('-').str[2]

print(subjcol)

samplemetadata['SAMPLE'] = samplecol
samplemetadata['SUBJID'] = subjcol

samplemetadata = pd.merge(samplemetadata, metadata, on='SUBJID')
samplemetadata['TISSUE'] = tissuecol
print(samplemetadata.head())

samplemetadata.to_csv(OUTDIR / "metadata.tsv", sep='\t', index=False)
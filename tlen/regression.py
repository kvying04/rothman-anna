import pandas as pd
from pathlib import Path
import numpy as np
import os
import math
from pathlib import Path
import statsmodels.formula.api as smf
import pyarrow.parquet as pq


ROOT = Path("/home/hanwenying")
DATADIR = ROOT / "rothman-data/transcriptlength"

metadata = pd.read_csv(DATADIR / 'dummy.tsv', sep='\t', dtype={'SAMPLE':str, 'SUBJID':str, 'TISSUE':str, 'AGE':int, 'SEX':int})
tpmdf = pd.read_parquet(DATADIR / 'tpm-gtex-v11.parquet', engine='pyarrow')

tpmthreshold = 10
tpmdf = tpmdf[tpmdf[metadata['SAMPLE']].T.mean() > tpmthreshold].reset_index()

tstatsdf = pd.DataFrame(columns=['GENE', 'TSTATISTIC', 'PVALUE'])

def lmm(i: int, row: pd.Series, metadata: pd.DataFrame):
	gene = row[1]
	y = row.reset_index()
	y = y.drop([0,1])
	y = y.rename(columns={'index':'SAMPLE', i:'TPM'})
	dm = pd.merge(y, metadata, on='SAMPLE')
	dm['TPM'] = dm['TPM'].astype(float)

	model = smf.mixedlm("TPM ~ AGE + SEX + TISSUE", dm, groups=dm['SUBJID'])
	res = model.fit()

	t,p = res.tvalues['AGE'], res.pvalues['AGE']
	return {"GENE":gene, "TSTATISTIC":t, "PVALUE":p}

for i, row in tpmdf.iterrows():
	print(f"{i}/{len(tpmdf)}", flush=True)
	tstatsdf.loc[len(tstatsdf)] = lmm(i, pd.Series(row), metadata)

tstatsdf.to_csv(DATADIR / "reg-t10.tsv", sep='\t', index=False)
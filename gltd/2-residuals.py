import pandas as pd
from pathlib import Path
import os
import scipy
import sys

ROOT = Path("/home/hanwenying")
DATA = ROOT / "rothman-data/gltd"
OUT  = ROOT / "rothman-anna/gltd/out"
BETA = OUT / "betas"
RESID = OUT / "resid"

id = int(os.environ.get("SLURM_ARRAY_TASK_ID", 0))

metadata = pd.read_csv(OUT / "metadata.tsv", sep='\t')

tissues_list = sorted(list(set(metadata['SMTSD'])))
tissue = tissues_list[id]

try:
	tissue_betas = pd.read_csv(BETA / f"{tissue}.tsv", sep='\t')

	m, b, _, _, _ = scipy.stats.linregress(tissue_betas['LOGLENGTH'], tissue_betas['BETA'])

	ypred = m * tissue_betas['LOGLENGTH'] + b
	resid = tissue_betas['BETA'] - ypred
	tissue_betas['RESIDUAL'] = resid

	tissue_betas.to_csv(RESID / f"{tissue}.tsv", sep='\t', index=False)
except FileNotFoundError:
	print(f"{tissue} does not exist in BETA folder.")
	sys.exit(1)
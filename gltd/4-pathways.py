import pandas as pd
from pathlib import Path
import numpy as np
import os
import gseapy as gp
import sys

ROOT = Path("/home/hanwenying")
DATA = ROOT / "rothman-data/gltd"
OUT  = ROOT / "rothman-anna/gltd/out"
BETA = OUT / "betas"
RESID = OUT / "resid"
GSEA = OUT / "gsea"

id = int(os.environ.get("SLURM_ARRAY_TASK_ID", 0))
nthreads = int(os.environ.get('SLURM_CPUS_PER_TASK', 1))

metadata = pd.read_csv(OUT / "metadata.tsv", sep='\t')
genesymbols = pd.read_csv(DATA / "ensembl_genesymbol_map.txt", sep='\t')

tissues_list = sorted(list(set(metadata['SMTSD'])))
tissue = tissues_list[id]

try:
	rnk = pd.read_csv(RESID / f"{tissue}.tsv", sep='\t')
except FileNotFoundError:
	print(f"{tissue}.tsv does not exist at RESID.")
	sys.exit(1)

kegg_symbols = gp.get_library(name='KEGG_2026', organism='Human')

ensembl = pd.DataFrame(rnk['GENE'].str.split('.').str[0])
ensembl.columns = ['ENSEMBL']
rnksymbols = pd.merge(ensembl, genesymbols, on='ENSEMBL').dropna(subset=['SYMBOL']).set_index('ENSEMBL')

rnk['GENE'] = ensembl
rnk = rnk.set_index('GENE')
rnk_gsea = rnk.join(rnksymbols).dropna(subset=['SYMBOL']).set_index('SYMBOL')

rnk_betas = rnk_gsea['BETA']
rnk_resid = rnk_gsea['RESIDUAL']

pr_betas = gp.prerank(rnk=rnk_betas,
				gene_sets='KEGG_2026',
				threads=nthreads,
				min_size=5,
				max_size=10000,
				permutation_num=5000,
				outdir=None,
				seed=24,
				verbose=True)

pr_resid = gp.prerank(rnk=rnk_resid,
				gene_sets='KEGG_2026',
				threads=nthreads,
				min_size=5,
				max_size=10000,
				permutation_num=5000,
				outdir=None,
				seed=24,
				verbose=True)

pr_betas.res2d.to_csv(GSEA / f"{tissue}_BETA.tsv", sep='\t', index=False)
pr_resid.res2d.to_csv(GSEA / f"{tissue}_RESID.tsv", sep='\t', index=False)
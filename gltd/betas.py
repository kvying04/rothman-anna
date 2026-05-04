import pyarrow.dataset as ds
import pandas as pd
from pathlib import Path
import numpy as np
import statsmodels.api as sm
import os
from tqdm import tqdm
import sys

ROOT = Path("/home/hanwenying")
DATA = ROOT / "rothman-data/gltd"
OUT  = ROOT / "rothman-anna/gltd/out"
BETA = OUT / "betas"

id = int(os.environ.get("SLURM_ARRAY_TASK_ID", 0))

gtex = ds.dataset(DATA / "tpm-gtex-v11.parquet", format="parquet")
genelengths = pd.read_csv(DATA / "gencode-v47-lengths.tsv", sep='\t')

genelengths = pd.DataFrame(genelengths.set_index('gene')['merged'])
genelengths['logmerged'] = np.log10(genelengths['merged'])

metadata = pd.read_csv(OUT / "metadata.tsv", sep='\t')

tissues_list = sorted(list(set(metadata['SMTSD'])))
tissue = tissues_list[id]
print(tissue)

if (BETA/f"{tissue}.tsv").is_file():
	print("This tissue has already been processed for BETAs.")
	sys.exit(0)

tissuesamples = metadata[metadata['SMTSD'] == tissue]

if len(tissuesamples) < 30:
	print(f"  Skipping {tissue}: only {len(tissuesamples)} samples with complete covariates")
	sys.exit(1)

samps_to_get = tissuesamples['SAMPID']
gtexdf = gtex.to_table(columns=list(samps_to_get) + ["Name"]).to_pandas()
gtexdf = gtexdf[gtexdf.index.isin(gtexdf.index.intersection(genelengths.index))]

tissue_exp = gtexdf[list(tissuesamples['SAMPID'])]
tissue_exp_log = np.log2(tissue_exp + 1)

highexp = ((tissue_exp_log > 0.5).sum(axis=1)) > 0.2 * tissue_exp.shape[1]
tissue_expdf = tissue_exp_log.loc[highexp]

tissue_summary = pd.DataFrame(columns=["GENE", 'LOGLENGTH', 'BETA', 'T', 'P'])

for gene in tqdm(tissue_expdf.index):
	genesummary = {'GENE': gene,
		 	'LOGLENGTH': genelengths.loc[gene]['logmerged']}
	y = tissue_expdf.loc[gene]
	X = pd.DataFrame({'INTERCEPT': np.ones(len(tissuesamples)), 'AGE':tissuesamples['AGE'], 'SEX':tissuesamples['SEX'], 'SAMPID': tissuesamples['SAMPID'], 'SMRIN': tissuesamples['SMRIN']}).set_index('SAMPID')

	model = sm.OLS(y, X)
	res = model.fit()

	beta_age, t, p = res.params['AGE'], res.tvalues['AGE'], res.pvalues['AGE']
	
	genesummary['BETA'] = beta_age
	genesummary['T'] = t
	genesummary['P'] = p

	tissue_summary.loc[len(tissue_summary)] = genesummary

tissue_summary.to_csv(BETA / f"{tissue}.tsv", sep='\t', index=False)
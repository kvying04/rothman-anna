import pandas as pd
from pathlib import Path
import numpy as np
import statsmodels.formula.api as smf

ROOT = Path('/home/hanwenying')
DATADIR = ROOT / "rothman-data/transcriptlength"

lengths = pd.read_csv(DATADIR / 'lengths.txt', sep='\t', usecols=['gene', 'merged'])
lengths['gene'] = lengths['gene'].str.split('.').str[0]
lengths.columns = ['GENE', 'LENGTH']

tstats = pd.read_csv(DATADIR / 'tstats-t10.tsv', sep='\t')
tstats['GENE'] = tstats['GENE'].str.split('.').str[0]

print(len(set(tstats['GENE']) - set(lengths['GENE'])))

dm = tstats.merge(lengths['GENE', 'LENGTH'], on='GENE', how='left')
del lengths, tstats

dm['LOGLENGTH'] = np.log(dm['LENGTH'])
dm = dm.dropna()

model = smf.ols("TSTATISTIC ~ LOGLENGTH", dm)
res = model.fit()

residuals = res.resid

forgsea = pd.DataFrame({"GENE": dm['GENE'], "RESIDUAL": residuals})
forgsea.to_csv(DATADIR / "reg-res.tsv", sep='\t', index=False)
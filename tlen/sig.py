from scipy.stats import spearmanr
import pandas as pd
from pathlib import Path

ROOT = Path("/home/hanwenying")
DATADIR = ROOT / "rothman-data/transcriptlength"

res = pd.read_csv(DATADIR / "pr_res.tsv", sep='\t', usecols=['Term', 'NES'])
t10 = pd.read_csv(DATADIR / "pr_t10.tsv", sep='\t', usecols=['Term', 'NES'])

res.columns = ['Term', 'NES_res']
res = pd.merge(res, t10, on="Term")
res.columns = ['Term', 'NES_res', 'NES_t10']

result = spearmanr(res['NES_res'].iloc[:50], res['NES_t10'].iloc[:50], alternative="two-sided")

print(result.statistic, result.pvalue)
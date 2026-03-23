import pandas as pd
from pathlib import Path
import pyarrow.parquet as pq

ROOT = Path("/home/hanwenying")
DATADIR = ROOT / "rothman-data/transcriptlength"

subjmd = pd.read_csv(DATADIR / "subjectmetadata-gtex-v11.txt", sep='\t')
samples = pd.Series(pq.read_schema(DATADIR / 'tpm-gtex-v11.parquet').names[1:-1])

subjparts = samples.str.split('-', expand=True)
subjrep = subjparts[0] + '-' + subjparts[1]
tissue = subjparts[2]

agemap = {'20-29': 0, '30-39': 1, '40-49': 2, '50-59': 3, '60-69': 4, '70-79': 5}
subjmd['AGE'] = subjmd['AGE'].map(agemap)

subjmd['SEX'] -= 1

metadata = pd.DataFrame({'SAMPLE':samples, 'SUBJID':subjrep, 'TISSUE':tissue})
metadata = metadata.merge(subjmd[['SUBJID', 'AGE', 'SEX']], on='SUBJID', how='left')

metadata.to_csv(DATADIR / 'dummy.tsv', sep='\t', index=False)
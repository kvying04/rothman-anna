import pandas as pd
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import os


DIR = Path("/Users/kvying/Files/ucsb-local")
LENGTHDIR = DIR / "rothman-anna/transcriptlength"
DATADIR = DIR / "rothman-data/anna/transcriptlength"
STRATDIR_METADATA = DATADIR / "metadata-stratified"
STRATDIR_TPM = DATADIR / "tpm-stratified"

rawtpms = pd.read_parquet(DATADIR / "tpm-gtex-v11.parquet", engine='pyarrow').reset_index()
metadata = pd.read_csv(DATADIR / "subjectmetadata-gtex-v11.txt", sep='\t')
agestrata = metadata['AGE'].unique()
sexstrata = metadata['SEX'].unique()

stratamap = {}

for age in agestrata:
	for sex in sexstrata:
		stratified = metadata.loc[(metadata["AGE"] == age) & (metadata["SEX"] == sex)]
		# stratified.to_csv(STRATDIR_METADATA / f"metadata_{sex}_{age}.tsv", sep='\t', index=False)
		stratamap[f"{sex}_{age}"] = list(stratified["SUBJID"])


def strattpm(raw: pd.DataFrame, agesex: str, subjlist: list[str], exportdir: Path) -> None:
	os.makedirs(exportdir, exist_ok=True)
	
	info = raw[['Name', 'Description']]
	strat = raw.loc[:, raw.columns[raw.columns.str.startswith(tuple(subjlist))]]
	tissues = np.unique(list(map(lambda sample: sample.split('-')[2], strat.columns)))

	for tissue in tissues:
		exportname = agesex + f"_{tissue}"
		tissuedf = strat.loc[:, strat.columns[strat.columns.str.split('-').str[2] == tissue]]
		tissuedf = pd.concat([info, tissuedf], axis=1)

		tissuedf.to_csv(exportdir / exportname, index=False, sep='\t')
	

	return



# with ProcessPoolExecutor(max_workers=8) as exec:

# print(rawtpms.head())

# with ProcessPoolExecutor(max_workers=8) as executor:
#     futures = [executor.submit(strattpm, rawtpms, agesex, stratamap[agesex], STRATDIR_TPM / agesex) for agesex in stratamap.keys()]
#     for future in futures:
#         future.result()

for agesex in stratamap.keys():
	strattpm(rawtpms, agesex, stratamap[agesex], STRATDIR_TPM / agesex)
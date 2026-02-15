import pandas as pd
from pathlib import Path

import gseapy as gp

# KEGG_2021_Human
# GO_Cellular_Component_2025
# GO_Biological_Process_2025
# GO_Molecular_Function_2025

genelist = []
genesets = ['KEGG_2021_Human', 'GO_Cellular_Component_2025', 'GO_Biological_Process_2025', 'GO_Molecular_Function_2025']

enr = gp.enrichr(gene_list=genelist, gene_sets=[])



# if __name__ == "__main__":
# 	ROOT = Path("/Users/kvying/Files/ucsb-local")
# 	DATADIR = ROOT / "rothman-data/anna/transcriptlength"

# 	rawtpms = pd.read_parquet(DATADIR / "tpm-gtex-v11.parquet", engine='pyarrow')


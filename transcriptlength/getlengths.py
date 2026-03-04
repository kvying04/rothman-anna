import sys
from pathlib import Path
import os

ROOT = Path("/home/hanwenying")
IMPORTDIR = os.path.abspath(ROOT / "rothman-sam/snps-pipeline")
DATADIR = ROOT / "rothman-data/anna/transcriptlength"
TLDIR = ROOT / "rothman-anna/transcriptlength"
OUTDIR = TLDIR / "out"

os.makedirs(OUTDIR, exist_ok=True)

sys.path.insert(1, IMPORTDIR)

import parsegtf

gtf = parsegtf.gtfdf(DATADIR / "hsa-ref.gtf")
locdf = parsegtf.getloc(gtf)

locdf.to_csv(OUTDIR / "locmap.tsv", sep='\t', index=False)
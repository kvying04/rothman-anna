ROOT="/home/hanwenying"
ARGUSDIR="$ROOT/rothman-anna/argus"
DATADIR="$ROOT/rothman-data/argus"
TRIMMEDDIR="$DATADIR/trimmed-fastq"

OUTDIR="$DATADIR/qc"

SEQS=("illumina" "aviti")

shopt -s extglob

for sub in "${SEQS[@]}"; do
	dir=$TRIMMEDDIR/$sub
	for fastq in $dir/*_trimmed.fastq?(.gz); do
		fastqc -o $OUTDIR/$sub --extract -t 6 $fastq
	done
	cd $OUTDIR/$sub
	multiqc .
done
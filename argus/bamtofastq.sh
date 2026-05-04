ROOT="/home/hanwenying"
ARGUSDIR="$ROOT/rothman-anna/argus"
DATADIR="$ROOT/rothman-data/argus"
BAMDIR="$DATADIR/raw-bams"

OUTDIR="$DATADIR/bam-fastq"

SEQS=("illumina" "aviti")

for sub in "${SEQS[@]}"; do
	dir=$BAMDIR/$sub
	for bam in $dir/*.bam; do
		prefix=$(basename "$bam" .bam)
		echo $prefix
		samtools sort -n -@ 8 -m 8G "$dir/$prefix.bam" | samtools fastq -@ 8 -1 "$OUTDIR/$sub/${prefix}_1.fastq.gz" -2 "$OUTDIR/$sub/${prefix}_2.fastq.gz" -
	done
done
ROOT="/home/hanwenying"
ARGUSDIR="$ROOT/rothman-anna/argus"
DATADIR="$ROOT/rothman-data/argus"
FASTQDIR="$DATADIR/raw-fastq"

OUTDIR="$DATADIR/trimmed-fastq"

# ILLUMINA_FASTQ="$FASTQDIR/illumina"
# AVITI_FASTQ="$FASTQDIR/aviti"

SEQS=("illumina" "aviti")

shopt -s extglob

# for dir in $FASTQDIR/*/; do
for sub in "${SEQS[@]}"; do
	dir=$FASTQDIR/$sub
	for fastq in $dir/*_1.fastq?(.gz); do
		prefix=$(basename "$fastq")
		prefix="${prefix%_1.fastq*}"

		rawprefix=$dir/$prefix
		outprefix=$OUTDIR/$sub/$prefix

		if [ -f "${rawprefix}_1.fastq.gz" ]; then
			ext=".fastq.gz"
		elif [ -f "${rawprefix}_1.fastq" ]; then
			ext=".fastq"
		fi
	

		if [ -f ${rawprefix}_2$ext ]; then # PE
			fastp --in1 "${rawprefix}_1${ext}" --in2 "${rawprefix}_2${ext}" \
			--out1 "${outprefix}_1_trimmed${ext}" --out2 "${outprefix}_2_trimmed${ext}" \
			-q 30 -e 30

		else # SE
			fastp -i "${rawprefix}_1${ext}" -o "${outprefix}_1_trimmed${ext}" \
			-q 30 -e 30
		fi
	done
done
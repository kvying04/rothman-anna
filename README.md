# Anna Stuff
> Last updated: 23 March 2026
## `argus`
`trim.sh`: Trims FASTQ files using FASTP.
`qc.sh`: FASTQ-wise quality control using FastQC; MultiQC report for each sequencing run.
## `tlen`
`metadata.py`: Generates metadata for linear models from GTEx.  
`regression.py`: TPM filtering ($\text{mean} \le 10$); gene-wise mixed linear regression with `TPM ~ AGE + SEX + TISSUE`, stratified by subject. Generate $t$-statistic for each gene. 
`residual.py`: Ordinary least squares (OLS) regression of $t$-statistic against merged exon length of gene. Generates residual value for each gene. 
`gsea.ipynb`: Gene set enrichment analysis (GSEA) of length-dependent and -independent gene rankings. Uses `KEGG_2026` gene set. 
`sig.py`: Spearman's rank correlation test to see difference between length-dependent and -independent enrichment ranking from GSEA. 

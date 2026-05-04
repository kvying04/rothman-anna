#!/bin/bash
#SBATCH --job-name=pathways
#SBATCH --output=logs/result_%a.out
#SBATCH --error=logs/error_%a.err
#SBATCH --ntasks=1
#SBATCH --mem=4G
#SBATCH --cpus-per-task=4
#SBATCH --array=0-67
#SBATCH --time=24:00:00


python3 pathways.py
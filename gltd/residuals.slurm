#!/bin/bash
#SBATCH --job-name=resids
#SBATCH --output=logs/result_%a.out
#SBATCH --error=logs/error_%a.err
#SBATCH --ntasks=1
#SBATCH --mem=2G
#SBATCH --array=0-67
#SBATCH --time=24:00:00


python3 residuals.py
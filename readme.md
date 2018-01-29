# Toxic Comment Kaggle 

## Text Cleaning Steps
Text cleaning is done first in python. `clean_lines.py` has a string parameter in the code that can be changed to point to either the traning data or a subset thereof. A sample file was created using `head - 1000 > train_sample.csv` and used for development before pointing to the full sized traning set. It runs quickly enough that I didn't bother to optimize.

## Visualization Steps
Covariance, co-occurence, and conditional probability matrices and heatmaps for the dummy labels are generated in `dummy_heat.R`'s environment.
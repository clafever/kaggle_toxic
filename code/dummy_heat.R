
library(tm)
library(dplyr)
library(tidyr)
library(ggplot2)
library(tibble)

# point to where the files are 
setwd("~/Desktop/kaggle_toxic/files")

# read the raw data
df_raw <- read.csv("train_cleaned.csv", header = T, sep = "|", stringsAsFactors = F)

df_raw %>% head

# lets look at the labels
df_labels <- df_raw[c("toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate")]

# sanity check - all severe toxic should be toxic of course - seems good ( you want 0 or might need to think about data quality )
toxic_check <- nrow(df_labels %>% filter(toxic == 0 && severe_toxic == 1))

# first, how they covary (co-occurence counts might be cool too but not as easy)
cov_labels <- cov(df_labels)
print(cov_labels)

# maybe lets make a heatmap
cov_labels_df <- data.frame(cov_labels) %>% rownames_to_column() %>% gather(key = "key", value = "value", c(toxic, severe_toxic, obscene, threat, insult, identity_hate))

# note that the diagonals are funky if it's not an "identity covariance" matrix - at least per intuition. Default pearson.
cov_labels_heat <- cov_labels_df %>% ggplot(aes(x=rowname, y=key, fill=value)) + geom_tile()

# also let's look at co-occurence
coc_labels <- as.matrix(df_labels) %>% crossprod()

# also prep this for heatmap
coc_labels_df <- data.frame(coc_labels) %>% rownames_to_column() %>% gather(key = "key", value = "value", c(toxic, severe_toxic, obscene, threat, insult, identity_hate))

# also heat. Note that this looks (of course) eerily similar to the covariances because what we intuitively want is conditional probabilities and this doesn't give it to us
# all severe toxic are toxic
coc_labels_heat <- coc_labels_df %>% ggplot(aes(x=rowname, y=key, fill=value)) + geom_tile()
print(coc_labels_heat)

# brute forcing conditional probabilities from this would be a fun exercise
# this brings shame to my family
get_total <- function(a_name,b_name) {
  cond <- coc_labels[a_name,b_name]
  tot <- coc_labels[b_name,b_name]
  return(cond/tot)
}

cp_list <- mapply(get_total,coc_labels_df$rowname, coc_labels_df$key)
coc_labels_cp_df <-cbind(coc_labels_df, cp_list) %>% select(pof = rowname, given = key, cp=cp_list)

coc_labels_cp_df %>% ggplot(aes(x=pof, y=given, fill=cp)) + geom_tile()


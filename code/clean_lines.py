# written by Chad LaFever and Peter James for Body by FORTRAN 
# Jan 2018: Initial development

# input: crap text file
# output: pipe delimited without junk newlines everywhere

# Hypothesis: if we scan over each line and strip any newlines, 
# we can simply append text into the file with no newlines until
# we reach the regex of 6 numbers with intersperced commas.

# In order to avoid replacing itermediate newlines such that 
# text is concatenated, we replace with a space (we could change the logic
# to only do this without the space when we encounter an EOL in the regex, however)

# Only needs to be good enough. Performance could be improved if needed by 
# reducing number of full scans

# could also possibly be done in one scan to make faster too but I like 
# the intermediate file for clarity and troubleshooting (just turn off cleanup)

# could also potentially write better regexes and pipe separate 
# as we scan (e.g. in the first step)

import re
import time
import os

# route wd to files folder at same level because I'm lazy and don't want to add elsewhere
os.chdir(os.path.join("..","files"))

# input file path
in_path = "train.csv"

# read the input path and fix it up
in_basename, in_extension = os.path.splitext(in_path)

# generate the output paths
aligned_path = "{0}{1}{2}".format(in_basename,"_aligned", in_extension)
cleaned_path = "{0}{1}{2}".format(in_basename,"_cleaned", in_extension)

# show on console
print "outputting aligned lines to: {0}".format(aligned_path)
print "outputting cleaned lines to: {0}".format(cleaned_path)

# useful regexes. start included only if needed
start_regex_string = "[a-z0-9]{16}"
end_regex_string = "(\,\d){6}"
text_regex_string = "{0}(.*?){1}".format(start_regex_string, end_regex_string)

start_regex = re.compile(start_regex_string)
end_regex = re.compile(end_regex_string)
text_regex = re.compile(text_regex_string)

# main logic to get lines all on same level
with open(in_path) as in_file, open(aligned_path, 'wb+') as aligned_file:
    header = in_file.readline()
    aligned_file.write(header)
    # skip the header
    # next(in_file)
    # iterate over the rest of the lines
    for line in in_file:
        # clean all newlines out
        clean_line = line.replace("\n", " ").replace("\r", " ")
        # conditional write depending on nature of segment we're looking at
        if end_regex.search(line):
            aligned_file.write(clean_line + "\n")
        else:
            aligned_file.write(clean_line)
# close the files
    in_file.close()
    aligned_file.close()

# now clean up all the excess apostrophes and commas
with open(aligned_path) as aligned_file, open(cleaned_path, "wb+") as cleaned_file:
    header = aligned_file.readline().replace(",","|")
    cleaned_file.write(header)
    # skip the header
    # next(aligned_file)
    for line in aligned_file:
        # print line
        # extract the id value
        id_value = re.search(start_regex, line).group()
        # extract the score values
        score_values = end_regex.search(line).group()
        # extract the "meat" of the line
        text_value = text_regex.search(line).group(1)
        # clean the middle values. we ultimately want pipe delimited
        clean_text_value = text_value.replace("|"," ")
        # smash together with pipes
        new_line = "|".join([id_value, text_value, score_values])
        # write to the file with a newline
        cleaned_file.write(new_line + "\n")
    aligned_file.close()
    cleaned_file.close()

# get rid of the middle file
print "Cleaning up intermediate file"
os.remove(aligned_path)

print "Dizzone"

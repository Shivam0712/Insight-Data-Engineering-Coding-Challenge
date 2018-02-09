# Insight Data Engineering Coding Challenge

# Summary and Instructions

This challenge is to do the following: 

1. Identify donations from repeat donors, defined as a donor (defined as a unique name & 5-digit zipcode combination) that has previously made a donation in any prior calendar year. 
2. For every donation from a repeat donor, calculate the following information for the recipient, zip code, and year of that donation: (1) running percentile of contributions from repeat donors, (2) total amount of donations from repeat donors, and (3) total number of donations from repeat donors.  

To run the code, execute run.sh as an executable.  The output of the programs can be found in the output folder as a text file labeled "repeat_donors.txt".

# Libraries Required

My code uses sys, datetime, and numpy libraries.

# Inputs

My code takes two inputs:

1. percentile.txt - text file that indicates the percentile to be calculated for donations from repeat donors.
2. itcont.txt - text file with contribution information.

For the itcont.txt file, the code uses six fields, with the following considerations:

* CMTE_ID: must not be empty
* NAME: must not be empty
* ZIP_CODE: must not be empty or have fewer than five digits
* TRANSACTION_DT: must not be empty and must be in a valid YYYYMMDD format
* TRANSACTION_AMT: must not be empty
* OTHER_ID: must be empty

# Approach

My code uses the following approach:

* Process the donation file one line at a time.  This avoids the memory required to read an entire file, in cases of large itcont.txt files.
* Filter out bad records.  The code does not import records with data that do not meet the considerations listed above.
* Use a DonorRecord object to keep track of key donor-level information, in order to determine whether a particular donation is from a repeat donor.
* Use a RecipientRecord object to keep track of information used to calculate outputs (i.e., all donations from repeat donors for a given CMTE_ID, ZIP_CODE, and year of TRANSACTION_DT)
* Use dictionaries to track DonorRecord and RecipientRecord objects.  Use of dictionaries enables rapid lookup of donors and recipients, even in cases of over 1,000,000 records.

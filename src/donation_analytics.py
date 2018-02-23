
## Author: Nadav Tanners
## Purpose: First, identify donations from repeat donors, defined as a 
## donor (defined as a unique name & 5-digit zipcode combination) that 
## has previously made a donation in any prior calendar year. 
## Second, for every donation from a repeat donor, calculate the 
## following information for the recipient, zip code, and year of that
## donation: (1) running percentile of contributions from repeat donors,
## (2) total amount of donations from repeat donors, and (3) total 
## number of donations from repeat donors.  
## Inputs: (1) A text file with the percentile to be calculated, and
## (2) a text file with the donations to be processed.  In the donations
## text file, the Columns of interest (with their placement in the text
## file) are:
##   CMTE_ID (0)
##   NAME (7)
##   ZIP_CODE (10)
##   TRANSACTION_DT (13)
##   TRANSACTION_AMT (14)
##   OTHER_ID (15)


import numpy as np
import sys
from datetime import datetime


class DonorRecord(object):
    
    def __init__(self, donor_id, donation_list):
        self.id = donor_id
        # min_year is used to set the value for repeat_donor.  
        self.min_year = donation_list[2]
        # flag used to indicate if the current donation being processed
        # is for a repeat donor.
        self.repeat_donor = False
        
    def add_donation(self, donation_list):
        # if the current donation being processed is from a later 
        # calendar year than min_year, set repeat_donor to True. 
        # Otherwise, set it to False.
        self.repeat_donor = donation_list[2] > self.min_year
        # update min_year, if necessary.
        if donation_list[2] < self.min_year:
            self.min_year = donation_list[2]
    
    
class RecipientRecord(object):
    
    def __init__(self, recipient_id, donor_id, donation_list, percentile):
        self.id = recipient_id
        self.amounts = [int(donation_list[3])]
        self.percentile = percentile
        
    def add_donation(self, donor_id, donation_list):
        self.amounts.append(int(donation_list[3]))
    
    def __str__(self):
        # generate the following output as a string: CMTE_ID, 5-digit 
        # ZIP_CODE, 4-digit year of contribution, running percentile of
        # contributions received, total amount of contributions 
        # received, and total number of contributions received 
        return '|'.join([self.id[0], self.id[1], self.id[2], 
                         str(np.percentile(self.amounts,self.percentile,
                                           interpolation='nearest')), 
                         str(sum(self.amounts)), str(len(self.amounts))])


def add_to_donor_dict(donor_dict, donor_id, donation_list):
    """
    function that checks to see if a donor has been added to donor_dict.
    If it has not been added, it creates a new DonorRecord and adds it 
    to donor_dict. If it has been added, it adds the latest donation 
    from that donor to the donor's DonorRecord in donor_dict.
    """
    if donor_dict.get(donor_id, None) is None:
        donor_dict[donor_id] = DonorRecord(donor_id, donation_list)
    else:
        donor_dict[donor_id].add_donation(donation_list)


def add_to_recipient_dict(recipient_dict, output, donor_id, donation_list,
                          percentile):
    """
    function that checks to see if a donation from a repeat donor has 
    been added to recipient_dict. If it has not been added, it creates a
    new RecipientRecord and adds it to recipient_dict. If it has been 
    added, it adds the latest donation to that recipient to the 
    recipient's RecipientRecord in recipient_dict.
    """
    # create a unique id for the recipient of this donation based on 
    # CMTE_ID, ZIP_CODE (5 digits), and TRANSACTION_DT (4-digit year)
    recipient_id = (donation_list[0], donation_list[1], str(donation_list[2]))
    # update recipient_dict with information from the latest donation 
    # from a repeat donor.
    if recipient_dict.get(recipient_id, None) is None:
        recipient_dict[recipient_id] = RecipientRecord(recipient_id, donor_id, 
                      donation_list, percentile)
    else:
        recipient_dict[recipient_id].add_donation(donor_id, donation_list)
    # after recipient_dict has been updated, append the latest output 
    # line to the output list.
    output.append(str(recipient_dict[recipient_id]))
    

def print_output(OUTPUT_PATH, output_list):
    """
    function that creates an output file with all of the output lines in
    the output list.
    """
    output_file = open(OUTPUT_PATH,"w")
    output_file.write("\n".join(output_list))
    output_file.close()


def summarize_repeat_donors(percentile, INPUT_PATH):
    """
    primary function that reads the donation records file, identifies
    repeat donors, and collects summary information about donations 
    from repeat donors into an output list.
    """
    with open(INPUT_PATH) as infile:
        
        # create dictionaries used to track donors and recipients
        donor_dict = {}
        recipient_dict = {}
        # create output list
        output = []
        for line in infile:
            # split each line into individual items and select only the 
            # relevant items: CMTE_ID, NAME, ZIP_CODE, TRANSACTION_DT, 
            # TRANSACTION_AMT, and OTHER_ID
            words = line.split("|")
            cmte_id = words[0]
            name = words[7]
            zip_code = words[10]
            transaction_dt = words[13]
            transaction_amt = words[14]
            other_id = words[15]
            # skip records with bad data.  All imported fields should be
            # non-blank, except for other_id, which should be blank.
            if (other_id is not "" or cmte_id == "" or name == "" 
                or len(zip_code) < 5 or transaction_dt == "" 
                or transaction_amt == ""): 
                continue
            
            # data processing steps: change the transaction_dt variable 
            # to a date data type (after making sure that it is a valid 
            # date), select the first five digits of the zip_code 
            # variable, create the unique identifier for the donor, and 
            # create a list with all relevant donor information
            try:
                transaction_dt = datetime.strptime(transaction_dt,'%m%d%Y')
            except:
                continue
            zip_code = zip_code[:5]
            donor_id = name + zip_code
            donation_list = [cmte_id, zip_code, transaction_dt.year, 
                             transaction_amt]
            
            # add the donation record to donor_dict, creating a new 
            # DonorRecord if one does not already exist for this 
            # donor_id.
            add_to_donor_dict(donor_dict, donor_id, donation_list)
            # if the current donation being processed is from a repeat 
            # donor, add the donation to recipient_dict, creating a new 
            # RecipientRecord if one does not already exist for this 
            # recipient_id.
            if donor_dict[donor_id].repeat_donor:
                add_to_recipient_dict(recipient_dict, output, donor_id, 
                                      donation_list, percentile)
    
    return output


def main():
    PERCENTILE_PATH = sys.argv[1]
    INPUT_PATH = sys.argv[2]
    OUTPUT_PATH = sys.argv[3]
    percentile = float(open(PERCENTILE_PATH).read())
    output = summarize_repeat_donors(percentile, INPUT_PATH)
    print_output(OUTPUT_PATH, output)

if __name__ == '__main__':
    main()

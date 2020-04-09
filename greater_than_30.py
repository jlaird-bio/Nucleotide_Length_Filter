#!/usr/bin/python

####################################################################################
#Recursively find all fastq files in a directory and reports each file name 
#and the percent of sequences in that file that are greater than 30 nucleotides long
#to the file greater_than_30.txt
####################################################################################

import os

fastq_dict = {}
def open_files(path):
    """
    recursively opens all files in a path
    reads files ending in .fastq
    removes the newline character
    splits fastq by every fourth line
    appends the file name and its reads to a dictionary
    """
    for path, dirs, files in  os.walk(path):
        for file_name in files:
            if ".fastq"  in file_name:
                fastq_open = open(path + "/" + file_name,"r")
                fastq_open = fastq_open.readlines()
                remove_newlines = [i.replace("\n","") for i in fastq_open]
                read_list =[]
                [read_list.append(remove_newlines[i:i+4]) for i in range(0, len(remove_newlines), 4)]
                fastq_dict[file_name] = read_list
    return fastq_dict

seq_count_dict = {}             
def count_sequences(dictionary):
    """
    loops through items in a dictionary 
    counts the total number of reads
    counts the number of reads over 30 
    appends the file name and the two read counts to a new dictionary
    """
    for key,value in dictionary.items():
        total_sequences = 0
        sequences_over_30 = 0
        for seq in value:
            if len(seq[1]) > 30:
                sequences_over_30 += 1
            else:
                total_sequences += 1
        seq_count_dict[key] = total_sequences, sequences_over_30
    return seq_count_dict

def report_percentages(dictionary):
    """
    creates the file greater_than_30.txt in working directory
    loops through items in dictionary
    divides the count of total reads by the count of reads over 30
    writes the file name and percent of reads over 30 to the greater_than_30.txt
    """
    report = open(r"./greater_than_30.txt", "w")
    for key,value in dictionary.items():
        percent_over_30 = str(float(value[0]) / value[1] * 100) + " %"
        report.write(key + ":" + "\n" + percent_over_30 + "\n\n")
    report.close()
        
#calls the functions with the necessary input          
open_files(r"./")
count_sequences(fastq_dict)
report_percentages(seq_count_dict)
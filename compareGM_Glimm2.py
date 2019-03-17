#!/usr/bin/env python3

import io
import sys
import re

GM = sys.argv[1]
Glimm = sys.argv[2]

GM_fhandle = io.open(GM,"r")
Glimm_fhandle = io.open(Glimm, "r")

#GM_first = GM_fhandle.readline()
#Glimm_first = Glimm_fhandle.readline()
#print (GM_first)
#print(Glimm_first)

def construct_GM_genes(fhandle):
    num = re.compile(r"^\s+\d")
    GM_genes = {}
    count = 1
    num_GM_genes = 0
    num_plus_genes = 0
    num_minus_genes = 0
    for line in fhandle:
        if re.search(num,line):
            splitline = line.split()
            GM_genes["gene" + str(count)] = {}
            GM_genes["gene"+str(count)]["strand"]=splitline[1]
            if splitline[1]=="+":
                GM_genes["gene"+str(count)]["start"]=splitline[2]
                GM_genes["gene"+str(count)]["stop"]=splitline[3]
                num_plus_genes += 1
            else:
                GM_genes["gene"+str(count)]["start"]=splitline[3]
                GM_genes["gene"+str(count)]["stop"]=splitline[2]
                num_minus_genes += 1
            count += 1
            num_GM_genes += 1
    GM_genes["plus strand genes"] = num_plus_genes
    GM_genes["minus strand genes"] = num_minus_genes
    GM_genes["total genes"] = num_GM_genes
    return GM_genes

def construct_Glim_genes(fhandle):
    Glim_genes = {}
    header = re.compile(r"^>")
    plus = re.compile(r"\+")
    count = 1
    num_Glim_genes = 0
    num_plus_genes = 0
    num_minus_genes = 0
    for line in fhandle:
        if re.search(header,line):
            continue
        splitline = line.split()
        Glim_genes["gene" + str(count)] = {}
        Glim_genes["gene"+str(count)]["strand"]=splitline[3]
        if re.search(plus,splitline[3]):
            Glim_genes["gene"+str(count)]["strand"]="+"
            Glim_genes["gene"+str(count)]["start"]=splitline[1]
            Glim_genes["gene"+str(count)]["stop"]=splitline[2]
            num_plus_genes += 1
        else:
            Glim_genes["gene"+str(count)]["strand"]="-"
            Glim_genes["gene"+str(count)]["start"]=splitline[1]
            Glim_genes["gene"+str(count)]["stop"]=splitline[2]
            num_minus_genes += 1
        count += 1
        num_Glim_genes += 1
    Glim_genes["plus strand genes"] = num_plus_genes
    Glim_genes["minus strand genes"] = num_minus_genes
    Glim_genes["total genes"] = num_Glim_genes
    return Glim_genes

GM_genes = construct_GM_genes(GM_fhandle)
Glim_genes = construct_Glim_genes(Glimm_fhandle)

def compare_gene_predictors(GM_genes, Glim_genes):
    """ Genes1 and Genes2 should be dictionaries for GM and glimmer genes
    Here - tring to first put all starts in a list, then compare them"""
    GM_starts = []
    Glim_starts = []
    GM_only = []
    Glim_only = []
    shared_starts = []
 #   GM_stops = []
 #   Glim_stops = []
    Glim_unique = 0
    GM_unique = 0

    for i in range(1,GM_genes["total genes"]+1):
        GM_starts.append(GM_genes["gene" + str(i)]["start"])
    for j in range(1,Glim_genes["total genes"]+1):
        Glim_starts.append (Glim_genes["gene"+ str(j)]["start"])
    for i in range(0,len(GM_starts)):
        if GM_starts[i] not in Glim_starts:
            print("start at pos. " + str(GM_starts[i]) + " is unique to GM genes")
            GM_only.append(GM_starts[i])
            GM_unique += 1
        else:
            shared_starts.append(GM_starts[i])
    for j in range(0,len(Glim_starts)):
        if Glim_starts[j] not in GM_starts:
            print ("start at pos. " + str(Glim_starts[j]) + " is unique to Glim genes")
            Glim_only.append(Glim_starts[j])
            Glim_unique += 1
        else:
            if GM_starts[j] not in shared_starts:
                shared_starts.append(GM_starts[j])
    shared_starts.sort()
    print ("Number of unique Glimmer starts = " + str(Glim_unique))
    print ("Number of unique GM starts = " + str(GM_unique))
    print("Shared starts =\n")
    for k in range(0,len(shared_starts)):
        print (shared_starts[k])


print("Number of Glimmer genes = " + str(Glim_genes["total genes"]))
print("Number of Glimmer plus strand genes = " + str(Glim_genes["plus strand genes"]))
print("Number of Glimmer minus strand genes = " + str(Glim_genes["minus strand genes"]))

print("Number of GM genes = " + str(GM_genes["total genes"]))
print("Number of GM plus strand genes = " + str(GM_genes["plus strand genes"]))
print("Number of GM minus strand genes = " + str(GM_genes["minus strand genes"]))

compare_gene_predictors(GM_genes, Glim_genes)
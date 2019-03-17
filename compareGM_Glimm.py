#!/usr/bin/env python3

""" this is the first vwesion of compare"""
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
    """ Genes1 and Genes2 should be dictionaries for GM and glimmer genes """
    for i in range(1,GM_genes["total genes"]):
        for j in range(1,Glim_genes["total genes"]):
            if GM_genes["gene" + str(i)]["start"] != Glim_genes["gene" + str(j)]["start"]:
                print ("GM_gene" + str(i) + "does not match a start in Glim_genes" )

        #for Glim_gene in Glim_genes:
        #    if GM_gene["start"] == Glim_gene["start"]:
        #       print (GM_gene + " matches " + Glim_gene)


print("Number of Glimmer genes = " + str(Glim_genes["total genes"]))
print("Number of Glimmer plus strand genes = " + str(Glim_genes["plus strand genes"]))
print("Number of Glimmer minus strand genes = " + str(Glim_genes["minus strand genes"]))

print("Number of GM genes = " + str(GM_genes["total genes"]))
print("Number of GM plus strand genes = " + str(GM_genes["plus strand genes"]))
print("Number of GM minus strand genes = " + str(GM_genes["minus strand genes"]))

compare_gene_predictors(GM_genes, Glim_genes)

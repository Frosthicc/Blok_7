import os
from setuptools import find_packages, setup

from Bio import NCBIWWW, NCBIXML
from ORF_parse_db import parse_database

header = "jantjepantje"
sequence = "attgaaagtcaatatttatcagactctaaaaaaattgttagagaaagaattattccttgggaaggattagcaagggctgaagttatatcggaggatgatgctaatcatattaaaattttagaaaagcagtcattagaaaataaaaattctact "
orf_sequence = "attgaaagtaatattatcagactctaaaaaaattgttagagaaagaattattccttgggaaggattagcaagggctgaagttatatcggaggatgatgctaat"
orf_startpos = 10
orf_endpos = 100



def main():
    blast_record = execute_BLASTp(sequence)
    accessioncodes, query_cover, organisms, protein_names, e_values, identities\
        = create_lists(blast_record)
    parse_database([header, sequence, orf_sequence, orf_startpos, orf_endpos, accessioncodes, query_cover, organisms, protein_names, e_values, identities], "blastx_results")

def execute_BLASTp(sequence):
    """"This function uses NCBIWWW.qblast to perform a blastx.
     It takes an sequence as input.
     It returns a blast_record as output.
     """

    print("Blasting sequence:", sequence)

    # result_handle = NCBIWWW.qblast("blastx", "nr", sequence)

    # with open("my_blast.xml", "w") as out_handle:
    #     out_handle.write(result_handle.read())
    # result_handle.close()

    result_handle = open("my_blast.xml")
    blast_record = NCBIXML.read(result_handle)

    return blast_record


def create_lists(blast_record):
    """"This function parses the information in the blast_record to
    multiple lists. There is an E-value cutoff of 1e-3 and a maximum
    of 10 alignments is safed.
    Input is the blast_record (execute_BLASTx)
    Output is multiple lists consisting of information about the blast
    results. """

    result_count = 0
    titles, accessioncodes, max_scores, query_cover, identities, gaps, \
    organisms, protein_names, sequence_header, lengths, e_values, \
    querys, matches, subjects = [], [], [], [], [], [], [], [], [], [], [], [], [], []
    for alignment in blast_record.alignments:
        for hsp in alignment.hsps:
            if result_count < 10:
                if hsp.expect < 1e-3:
                    titles.append(alignment.title.replace("'", ""))
                    accessioncodes.append(alignment.accession)
                    max_scores.append(hsp.bits)
                    query_cover.append(float((hsp.query_end -
                                              hsp.query_start)
                                             / 300) * 100)
                    identities.append(
                        (hsp.identities / hsp.align_length)
                        * 100)
                    gaps.append(hsp.gaps)
                    if alignment.title[0:2] == 'gi':
                        organisms.append(alignment.title.split(">")[0]
                                         .split("|")[4].split("[")[1]
                                         [:-1].strip("]")
                                         .replace("'", ""))
                    else:
                        organisms.append(alignment.title.split(">")[0]
                                         .split("|")[2].split("[")[1]
                                         [:-1].strip("]")
                                         .replace("'", ""))
                    protein_names.append(alignment.title.split("|")[2]
                                         .split("[")[0][1:]
                                         .replace("'", ""))
                    lengths.append(alignment.length)
                    e_values.append(hsp.expect)
                    querys.append(hsp.query)
                    matches.append(hsp.match)
                    subjects.append(hsp.sbjct)
                    result_count += 1

    return accessioncodes, query_cover, organisms, protein_names, e_values, identities

main()
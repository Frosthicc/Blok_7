""""
ORF_blast
Datum: 09-04-2020
Auteur: Bart Jolink
"""

from Bio.Blast import NCBIWWW, NCBIXML
from ORF_parse_db import parse_database, temp_reader

def main():
    header, sequence, orfseqs, startpos, endpos = temp_reader()
    for i in range(len(orfseqs)):
        blast_record = execute_BLASTp(orfseqs[i])
        accessioncodes, query_cover, organisms, protein_names, e_values, identities\
            = create_lists(blast_record)
        parse_database([header, sequence, orfseqs[i], startpos[i], endpos[i], accessioncodes, query_cover, organisms, protein_names, e_values, identities], "blastx_results")


def execute_BLASTp(sequence):
    """"This function uses NCBIWWW.qblast to perform a blastx.
     It takes an sequence as input.
     It returns a blast_record as output.
     """

    print("Blasting sequence:", sequence)

    result_handle = NCBIWWW.qblast("blastx", "nr", sequence)

    with open("my_blast.xml", "w") as out_handle:
        out_handle.write(result_handle.read())
    result_handle.close()

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
    print(blast_record)
    result_count = 0
    accessioncodes, query_cover, identities, organisms, protein_names, e_values\
        = [], [], [], [], [], []
    for alignment in blast_record.alignments:
        for hsp in alignment.hsps:
            if result_count < 10:
                accessioncodes.append(alignment.accession)
                query_cover.append(float((hsp.query_end -
                                          hsp.query_start)
                                         / 300) * 100)
                identities.append(
                    (hsp.identities / hsp.align_length)
                    * 100)
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
                e_values.append(hsp.expect)
                result_count += 1

    print(accessioncodes, query_cover, organisms, protein_names, e_values, identities)
    return accessioncodes, query_cover, organisms, protein_names, e_values, identities

main()
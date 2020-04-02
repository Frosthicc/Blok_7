import mysql.connector
from datetime import date


def parse_database(list, method):
    if method == "blastx_results":
        parse_blastx_results(list)

    if method == "orf_results":
        parse_orf_results(list)

    if method == "sequence":
        parse_sequence(list)

    if method == "organism":
        parse_organism(list)

    if method == "protein":
        parse_protein(list)

    if method == "reference_seq":
        parse_reference_seq(list)

    if method == "reference_header":
        parse_reference_header(list)

    if method == "information":
        parse_information(list)

def parse_blastx_results(list):
    header, sequence, orf_sequence, orf_startpos, orf_endpos, \
    accessioncodes, query_cover, organisms, protein_names, e_values, identities \
        = list[0], list[1], list[2], list[3], list[4], list[5],\
          list[6], list[7], list[8], list[9], list[10]

    orf_id = get_orf_id(orf_sequence)
    if orf_id is None:
        parse_database([header, sequence, orf_sequence,
                        orf_startpos, orf_endpos], "orf_results")
        orf_id = get_orf_id(orf_sequence)

    for i in range(len(accessioncodes)):
        org_id = get_org_id(organisms[i])
        if org_id is None:
            parse_database([organisms[i]], "organism")
            org_id = get_org_id(organisms[i])

        prot_id = get_prot_id(protein_names[i])
        if prot_id is None:
            parse_database([protein_names[i]], "protein")
            prot_id = get_prot_id(protein_names[i])

        cursor, sql_connection = get_cursor()
        cursor.execute("insert into blastx_results(blast_id, orf_id, org_id, prot_id, accessiecode, querycover, evalue, identity)"
"values(null, '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(orf_id[0], org_id[0], prot_id[0], accessioncodes[i], query_cover[i], e_values[i], identities[i]))
        sql_connection.commit()
        cursor.close()
        sql_connection.close()


def parse_orf_results(list):
    header, sequence, orf_sequence, orf_startpos, orf_endpos = list[0], list[1], list[2], list[3], list[4]

    seq_id = get_seq_id(sequence)
    if seq_id is None:
        parse_database([header, sequence], "sequence")
        seq_id = get_seq_id(sequence)
    else:
        print("ja")
        update_information(seq_id[0])

    cursor, sql_connection = get_cursor()
    cursor.execute("insert into orf_results(orf_id, seq_id, orf_start, orf_stop, orf_sequence)"
                   "values(null, '{}', '{}', '{}', '{}');"
                   .format(seq_id[0], orf_startpos, orf_endpos, orf_sequence))
    sql_connection.commit()
    cursor.close()
    sql_connection.close()


def parse_sequence(list):
    header, sequence = list[0], list[1]

    seq_id = get_seq_id(sequence)
    if seq_id is None:
        print("nee")
        parse_database([sequence], "reference_seq")
        refseq_id = get_refseq_id(sequence)
        parse_database([header], "reference_header")
        refheader_id = get_refheader_id(header)
        cursor, sql_connection = get_cursor()
        cursor.execute("insert into sequence(seq_id, refseq_id, refheader_id)"
                       "values(null, '{}', '{}');"
                       .format(refseq_id[0], refheader_id[0]))
        sql_connection.commit()
        cursor.close()
        sql_connection.close()

        seq_id = get_seq_id(sequence)[0]
        parse_database([seq_id], "information")


def parse_organism(list):
    organism = list[0]

    org_id = get_org_id(organism)
    if org_id is None:
        cursor, sql_connection = get_cursor()
        cursor.execute(
            "insert into organism(org_id, organism_name)"
            "values(null, '{}');"
            .format(organism))
        sql_connection.commit()
        cursor.close()
        sql_connection.close()


def parse_protein(list):
    protein = list[0]

    prot_id = get_prot_id(protein)
    if prot_id is None:
        cursor, sql_connection = get_cursor()
        cursor.execute(
            "insert into protein(prot_id, prot_name)"
            "values(null, '{}');"
            .format(protein))
        sql_connection.commit()
        cursor.close()
        sql_connection.close()


def parse_reference_seq(list):
    sequence = list[0]

    refseq_id = get_refseq_id(sequence)
    if refseq_id is None:
        cursor, sql_connection = get_cursor()
        cursor.execute(
            "insert into reference_seq(refseq_id, sequence)"
            "values(null, '{}');"
            .format(sequence))
        sql_connection.commit()
        cursor.close()
        sql_connection.close()

    cursor, sql_connection = get_cursor()

    cursor.execute(
        "select seq_id "
        "from sequence "
        "where refseq_id = ( select refseq_id "
        "                       from reference_seq "
        "                       where sequence = '{}'"
        "                       limit 1);".format(
            sequence))
    results = cursor.fetchone()
    cursor.close()
    sql_connection.close()


def parse_reference_header(list):
    header = list[0]

    refheader_id = get_refheader_id(header)
    if refheader_id is None:
        cursor, sql_connection = get_cursor()
        cursor.execute(
            "insert into reference_header(refheader_id, Header)"
            "values(null, '{}');"
            .format(header))
        sql_connection.commit()
        cursor.close()
        sql_connection.close()


def parse_information(list):
    seq_id = list[0]
    print(seq_id)
    print(seq_id)
    today = date.today()

    print(today)

    cursor, sql_connection = get_cursor()
    cursor.execute(
        "insert into information(submission, seq_id, created, last_update)"
        "values(0, '{}', '{}', '{}');"
            .format(seq_id, today, today))
    sql_connection.commit()
    cursor.close()
    sql_connection.close()

def update_information(seq_id):
    today = date.today()

    print(today)

    cursor, sql_connection = get_cursor()
    cursor.execute(
        "UPDATE information "
        "SET last_update = '{}' "
        "where seq_id = '{}';"
            .format(today, seq_id))
    sql_connection.commit()
    cursor.close()
    sql_connection.close()

def get_seq_id(sequence):
    cursor, sql_connection = get_cursor()

    print(sequence)
    cursor.execute(
        "select seq_id "
        "from sequence "
        "where refseq_id = ( select refseq_id "
        "                       from reference_seq "
        "                       where sequence = '{}'"
        "                       limit 1);".format(
            sequence))
    results = cursor.fetchone()
    cursor.close()
    sql_connection.close()

    print(results)


    return results

def get_refseq_id(sequence):
    cursor, sql_connection = get_cursor()

    cursor.execute(
        "select refseq_id "
        "from reference_seq "
        "where sequence = '{}'"
        "                       limit 1;".format(
            sequence))
    results = cursor.fetchone()
    cursor.close()
    sql_connection.close()

    return results


def get_refheader_id(header):
    cursor, sql_connection = get_cursor()

    cursor.execute(
        "select refheader_id "
        "from reference_header "
        "where header = '{}'"
        "                       limit 1;".format(
            header))
    results = cursor.fetchone()
    cursor.close()
    sql_connection.close()

    return results


def get_orf_id(orf_sequence):
    cursor, sql_connection = get_cursor()

    cursor.execute(
        "select orf_id "
        "from orf_results "
        "where orf_sequence = '{}'"
        "                       limit 1;".format(
            orf_sequence))
    results = cursor.fetchone()

    cursor.close()
    sql_connection.close()

    return results


def get_org_id(organism):
    cursor, sql_connection = get_cursor()

    cursor.execute(
        "select org_id "
        "from organism "
        "where organism_name = '{}'"
        "                       limit 1;".format(
            organism))
    results = cursor.fetchone()

    cursor.close()
    sql_connection.close()

    return results


def get_prot_id(protein):
    cursor, sql_connection = get_cursor()

    cursor.execute(
        "select prot_id "
        "from protein "
        "where prot_name = '{}'"
        "                       limit 1;".format(
            protein))
    results = cursor.fetchone()

    cursor.close()
    sql_connection.close()

    return results


def set_connection():
    """"This function sets a connection to a database (Ossux).
    (During blasting password input was pre-filled. For privacy reasons,
    the password was changed to an input field)
    Input is a password.
    Output is an SQL_connection.
    """

    sql_connection = mysql.connector.connect(
        host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com",
        user="owe7_pg3@hannl-hlo-bioinformatica-mysqlsrv",
        db="Owe7_pg3",
        password="blaat1234")

    return sql_connection


def get_cursor():
    sql_connection = set_connection()
    cursor = sql_connection.cursor(buffered=True)

    return cursor, sql_connection

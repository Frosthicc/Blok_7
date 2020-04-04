# Author       : Paul Verhoeven
# Version      : 1.0
# Date         : 2020-01-04
# last update  : 2020-04-04

from objects import Orf, Seq
import sys


def load_sequence():
    """
    Reads the .fasta file selected by the user.
    :return: An initiated Seq object containing a files header and string
    """
    seq = ''
    header = ''
    file = sys.argv[1]
    with open(file, 'r') as file:
        for line in file:
            line = line.strip('\n')
            if line.startswith('>'):
                header = line
            else:
                seq += line.lower()

    return Seq(seq, header)


def predict_orf(data):
    """
    Creates 3 Open reading frames objects with sequences, starting position and stop position relative to the input
    sequence.
    :param data: Seq object initiated in load_sequence() function
    :return: List with Orf objects
    """
    if 'u' in data.get_seq():
        data.rna_to_dna()
    seq = data.get_seq()
    orf_data = []
    orf_building = []
    # init building list
    for i in range(3):
        orf_building.append([False, 0, ''])

    # start looking for ORFs
    for i in range(0, len(seq), 3):
        frame = [seq[i:i + 3], seq[i - 2: i + 1], seq[i - 1: i + 2]]
        start = [i+1, i-1, i]
        stop = [i+3, i+1, i+2]

        for x in range(len(frame)):
            if frame[x] == 'atg':
                orf_building[x][2] += frame[x]
                if not orf_building[x][0]:
                    orf_building[x][1] = start[x]
                orf_building[x][0] = True

            elif orf_building[x][0]:
                orf_building[x][2] += frame[x]
                if frame[x] in ['tga', 'taa', 'tag']:
                    orf_data.append(Orf(orf_building[x][1], stop[x], orf_building[x][2]))
                    orf_building[x][0] = False

    return orf_data


def write_data(data, orf_data):
    """
    Writes the created data to a textfile
    :param data: Seq object initiated in load_sequence() function
    :param orf_data: List with Orf objects initiated in predict_orf() function
    """
    with open(sys.argv[2], 'w') as save:
        save.write(data.get_info())
        for i in range(len(orf_data)):
            save.write(orf_data[i].get_object_data())
            save.write('\n')
        save.write('\n')


def main():
    data = load_sequence()
    orf_data = predict_orf(data)
    write_data(data, orf_data)


main()

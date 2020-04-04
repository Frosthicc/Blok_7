from objects import Orf, Seq
import sys

def load_sequence():
    seq = ''
    header = ''
    file = sys.argv[1]
    with open(file, 'r') as file:
        for line in file:
            line = line.strip('\n')
            if line.startswith('>'):
                header = line
            else:
                seq += line

    # Returns a Seq object
    return Seq(seq, header)


def predict_orf(data):
    if 'u' in data.get_seq():
        data.rna_to_dna()
    seq = data.get_seq()
    orf_data = []
    orf_seq = []
    for i in range(0, len(seq), 3):
        frame_1 = seq[i:i + 3]
        frame_2 = seq[i - 2: i + 1]
        frame_3 = seq[i - 1: i + 2]

        if len(frame_1) == 3:
            if len(orf_data) == 0:
                orf_data.append(Orf(i+1, i+3, ''))
                orf_seq.append(frame_1)
            else:
                orf_seq[0] += frame_1
                orf_data[0].set_endpos(i+3)

        if len(frame_2) == 3:
            if len(orf_data) == 1:
                orf_data.append(Orf(i-1, i+1, ''))
                orf_seq.append(frame_2)
            else:
                orf_seq[1] += frame_2
                orf_data[1].set_endpos(i+1)

        if len(frame_3) == 3:
            if len(orf_data) == 2:
                orf_data.append(Orf(i, i+2, ''))
                orf_seq.append(frame_3)
            else:
                orf_seq[2] += frame_3
                orf_data[2].set_endpos(i+2)

    for i in range(len(orf_data)):
        orf_data[i].set_frameseq(orf_seq[i])
    del orf_seq
    return orf_data


def write_data(data, orf_data):
    with open('placeholder.txt', 'a') as save:
        save.write(data.get_info())
        for i in range(len(orf_data)):
            save.write(orf_data[i].get_object_data())
            save.write('\n')


def main():
    data = load_sequence()
    orf_data = predict_orf(data)
    write_data(data, orf_data)


main()

# Author       : Paul Verhoeven
# Version      : 1.0
# Date         : 2020-01-04
# last update  : 2020-01-04


class Seq(object):
    def __init__(self, sequence, header):
        """
        Sets local variables to retrieved file data.
        :param sequence: A DNA/RNA sequence input.
        :param header: A header from fasta file.
        """
        self._sequence = sequence
        self._header = header

    def rna_to_dna(self):
        """
        A method that turns RNA strand into DNA strand
        """
        self._sequence = self._sequence.replace('u', 't')

    def get_header(self):
        """
        :return: Set header from input file.
        """
        return self._header

    def get_seq(self):
        """
        :return: Set sequence from input file.
        """
        return self._sequence

    def get_info(self):
        """
        :return: A string with header and sequence, mainly used for the write function in Orf_finder.py
        """
        return f'{self.get_header()}\t{self.get_seq()}\n'


class Orf(object):
    def __init__(self, start, stop, seq):
        """
        :param start: Sequence starting position
        :param stop: Sequence Stop position
        :param seq: ORF sequence based on file input sequence.
        """
        self._startpos = start
        self._endpos = stop
        self._frameseq = seq

    def set_startpos(self, position):
        """
        Sets start position variable to input
        :param position: int start position
        """
        self._startpos = position

    def set_endpos(self, position):
        """
        Sets stop position variable to input
        :param position: int stop position
        """
        self._endpos = position

    def set_frameseq(self, seq):
        """
        ORF sequence input
        :param seq: Sets relative ORF sequence
        """
        self._frameseq = seq

    def get_startpos(self):
        """
        :return: Returns ORF start position
        """
        return self._startpos

    def get_endpos(self):
        """
        :return: Returns ORF stop position
        """
        return self._endpos

    def get_frameseq(self):
        """
        :return: Returns the ORF sequence
        """
        return self._frameseq

    def get_object_data(self):
        """
        :return: A string with sequence, start position and stop position, mainly used for the write function in
        Orf_finder.py
        """
        return f'{self._frameseq}\t{self._startpos}\t{self._endpos}'


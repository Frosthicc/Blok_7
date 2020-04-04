# Author       : Paul Verhoeven
# Version      : 1.0
# Date         : 2020-01-04
# last update  : 2020-01-04


class Seq(object):
    def __init__(self, sequence, header):
        self._sequence = sequence
        self._header = header

    def rna_to_dna(self):
        self._sequence = self._sequence.replace('u', 't')

    def get_header(self):
        return self._header

    def get_seq(self):
        return self._sequence

    def get_info(self):
        return f'{self.get_header()}\n{self.get_seq()}\n'


class Orf(object):
    def __init__(self, start, stop, seq):
        self._startpos = start
        self._endpos = stop
        self._frameseq = seq

    def set_startpos(self, position):
        self._startpos = position

    def set_endpos(self, position):
        self._endpos = position

    def set_frameseq(self, seq):
        self._frameseq = seq

    def get_startpos(self):
        return self._startpos

    def get_endpos(self):
        return self._endpos

    def get_frameseq(self):
        return self._frameseq

    def get_object_data(self):
        return f'{self._frameseq}\t{self._startpos}\t{self._endpos}'


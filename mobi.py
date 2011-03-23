import struct
import time

from basebook import BaseBook


class MobiBook(BaseBook):
    def output_to_file(self, filename):
        output = open(filename, 'wb')
        self._write_palmdoc_header()
        self._write_mobi_header()
        self._write_exth_header()

        self._write_pdb_wrapper(output)
        output.close()

    def _write_palmdoc_header(self, output):
        record_count = 0
        text_length = 0

        values = [
            1, # Compression (1=None)
            0, # Unused
            text_length, # Text length of entire book
            record_count, # PDB record count
            4096, # PDB record max. size (always 4096)
            0, # Encryption (0=None)
            0, # Unknown (always 0)
        ]

        struct.pack('>')

    def _write_pdb_wrapper(self, output):
        format = '>32shhLLLlll4s4sllh'

        title = self._mobi_title()
        mobi_date = self._mobi_now()
        num_records = 0

        values = (
            title, # Book title
            0, # File attribute
            0, # File version
            mobi_date, # Creation date
            mobi_date, # Modification date
            0, # Last backup date
            0,
            0,
            0,
            'BOOK', # Type
            'MOBI', # Program
            0, # uniqueIDseed
            0, # Always 0
            num_records # No. of records
        )

    def _mobi_now(self):
        OFFSET = 2082844800L
        return int(time.time()+OFFSET)

    def _mobi_title(self):
        title = ''
        for i in range(32):
            c = self.title[i]
            if c == ' ':
                c = '_'
            if ord(c) < 128:
                title += c
            else:
                title += '{:x}'.format(ord(c))
        return title
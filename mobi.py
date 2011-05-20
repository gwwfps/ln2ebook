import struct
import time

from basebook import BaseBook
from epub import EpubBook


class MobiBook(EpubBook):
    def out_to_file(self, filename, args):
        super(EpubBook, self).output_to_file(filename, args)
        if not args.kindlegen:
            print 'Need kindlegen path'
            exit()



class RealMobiBook(BaseBook): # WIP
    def output_to_file(self, filename, args):
        output = open(filename, 'wb')
        self._write_palmdoc_header()
        self._write_mobi_header()
        self._write_exth_header()

        self._write_pdb_wrapper(output)
        output.close()

    def _write_palmdoc_header(self, output):
        format = '>2hl4h4s5l40s13l'

        record_count = 0
        text_length = 0
        header_length = 0
        unique_id = 0

        values = (
            1, # Compression (1=None)
            0, # Unused
            text_length, # Text length of entire book
            record_count, # PDB record count
            4096, # PDB record max. size (always 4096)
            0, # Encryption (0=None)
            0, # Unknown (always 0)
            'MOBI', # Always 'MOBI'
            header_length, # MOBI header length
            2, # MOBI type
            65001, # Encoding (65501=UTF-8)
            unique_id, # Unique ID
            6, # MOBI format version
            '\xff'*40, # Reserved
            
        )

        struct.pack(format, *values)

    def _write_pdb_header(self, output):
        format = '>32s2h3L3l4s4s2lh'

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
        for c in self.title:
            if len(title) > 31:
                break
            if c == ' ':
                c = '_'
            if ord(c) < 128:
                title += c
            else:
                title += '{:x}'.format(ord(c))
        return title
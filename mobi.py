import struct

from basebook import BaseBook


class MobiBook(BaseBook):
    def output_to_file(self, filename):
        output = open(filename, 'wb')
        self._write_palmdoc_header()
        self._write_mobi_header()
        self._write_exth_header()

        self._write_pdb_wrapper()
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
        values = [
            title, # Book title
            2, # File attribute (0x0002=Read-only)
            1, # File version
            
        ]

        
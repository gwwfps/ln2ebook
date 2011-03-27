import zipfile

from basebook import BaseBook
from utils import render


class EpubBook(BaseBook):
    def output_to_file(self, filename, args):
        output = zipfile.ZipFile(filename, 'w')
        self._write_mimetype(output)
        self._write_meta_inf(output)
        self._write_title(output)
        self._write_chapters(output)
        self._write_images(output)
        self._write_opf(output)
        self._write_ncx(output)
        output.close()

    def _write_mimetype(self, output):
        output.writestr('mimetype', render('epub/mimetype'),
                        compress_type=zipfile.ZIP_STORED)

    def _write_meta_inf(self, output):
        output.writestr('META-INF/container.xml', render('epub/container.xml'))

    def _write_title(self, output):
        output.writestr('OEBPS/title.html',
                        render('epub/title.html', title=self.title,
                               has_cover=self.has_cover))

    def _write_chapters(self, output):
        for i in range(len(self.chapters)):
            output.writestr('OEBPS/ch-{}.html'.format(i+1),
                            render('epub/chapter.html',
                                   title='Chapter {}'.format(i+1),
                                   content=self.chapters[i]))

    def _write_images(self, output):
        for i in range(len(self.images)):
            filename, image = self.images[i]
            if not i:
                output.writestr('OEBPS/images/cover.jpg', image)
            output.writestr('OEBPS/{}'.format(filename), image)

    def _write_opf(self, output):
        output.writestr('OEBPS/content.opf',
                        render('epub/meta.opf',
                               bookid=self.bookid,
                               title=self.title,
                               has_cover=self.has_cover,
                               num_chapters=len(self.chapters)))

    def _write_ncx(self, output):
        output.writestr('OEBPS/toc.ncx',
                        render('epub/toc.ncx',
                               bookid=self.bookid,
                               title=self.title,
                               num_chapters=len(self.chapters)))
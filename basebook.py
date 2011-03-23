class BaseBook(object):
    def __init__(self, title, chapters, images, bookid):
        self.title = title
        self.chapters = chapters
        self.images = images
        self.bookid = bookid
        self.has_cover = bool(images)
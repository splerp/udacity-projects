from datetime import date


class Movie:
    """
    Defines a movie object to store all relevant movie information.

    Stores a unique ID, a title, release date, genre,
    youtube video ID, and short and long descriptions.
    """

    # Default values for info, when something is not provided.
    id = "0000 Unknown"

    title = ""
    release_date = date(1, 1, 1)
    genre = "Unknown"

    trailer_youtube_id = "hP4WsVHTVh0"

    short_description = ""
    long_description = ""

    def __init__(self, *args, **kwargs):
        """
        Handles receiving all values and assigning them to the
        correct variables.
        """

        if('id' in kwargs):
            self.id = kwargs['id']

        if('title' in kwargs):
            self.title = kwargs['title']
        if('rd' in kwargs):
            self.release_date = kwargs['rd']
        if('genre' in kwargs):
            self.genre = kwargs['genre']

        if('vidid' in kwargs):
            self.trailer_youtube_id = kwargs['vidid']

        if('sdesc' in kwargs):
            self.short_description = kwargs['sdesc']
        if('ldesc' in kwargs):
            self.long_description = kwargs['ldesc']

    def to_string(self):
        """
        Creates a text version of the movie, showing the title and
        release year.
        """
        return "" + self.title + " (" + self.release_date.strftime('%Y') + ")"

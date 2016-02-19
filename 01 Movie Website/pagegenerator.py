import webbrowser
import os
import re

# A single movie entry html template
movie_tile_content = '''
<div class="col-xs-4 movie-tile text-center"
data-trailer-youtube-id="{trailer_youtube_id}"
data-long-desc="{movie_long_desc}"
data-toggle="modal"
data-target="#trailer">
    <img src="{poster_image_url}" width="220">
    <h2>{movie_title} ({release_date})</h2>
    <div class="shortdesc">{movie_short_desc}</div>
    <div class="longdesc">{movie_long_desc}</div>
</div>
'''


def create_genre_list_content(genres):
    # Creates an HTML unordered list out of the available genres.

    to_return = '<ul>'

    # Creates the special case "All" genre, used to display all movies.
    name = "All"
    to_return += '<li data-genre="All">All</li>'

    # Creates elements for each genre passed in.
    for name in genres:
        to_return += '<li data-genre="' + name + '">' + name + '</li>'

    # Creates the special case "Unknown" genre, for movies without a genre.
    to_return += '<li data-genre="Unknown">Unknown</li>'

    to_return += '</ul>'
    return to_return


def begin_genre_content(genre):
    # Creates the beginning of a group of movies ("genre-section").

    return '''
    <div id="genre-{genrename}" class="container genre-section">
    <h1>{genrename}</h1>
    '''.format(genrename=genre)


def end_genre_content():
    # Returns all code required to complete the genre content div.

    return "</div>"


def create_movie_sections_content(movies, genres):
    # Create the HTML content for the entire movie list section.

    # Create a dict to store each genre's HTML content.
    genre_contents = {}

    # Begin genre content for special case genre "All".
    genre_contents["All"] = begin_genre_content("All")

    # Set up initial genre content for all known genres.
    for g in genres:
        genre_contents[g] = begin_genre_content(g)

    # Begin genre content for special case genre "Unknown".
    genre_contents["Unknown"] = begin_genre_content("Unknown")

    for movie in movies:

        # Creates the movie content by formatting the movie content variable.
        movie_content = movie_tile_content.format(
                        movie_title=movie.title,
                        release_date=movie.release_date.strftime('%Y'),
                        poster_image_url=getPosterImageURL(movie),
                        trailer_youtube_id=movie.trailer_youtube_id,
                        movie_short_desc=movie.short_description,
                        movie_long_desc=movie.long_description
                    )

        # Search for the specified genre.
        found = False
        for g in genres:
            if(movie.genre == g):
                # Append the tile for the movie with its content filled in
                genre_contents["All"] += movie_content
                genre_contents[g] += movie_content
                found = True

        # If not found, add to the "Unknown" category.
        if not found:
            genre_contents["All"] += movie_content
            genre_contents["Unknown"] += movie_content

    # Create a new variable to contain the final movie section HTML.
    content = ''

    # Loop through each genre and append to the content variable.
    for key, value in genre_contents.items():
        value += end_genre_content()
        content += value

    return content


def open_movies_page(movies, genres):
    # Given a movie list and genre list, this function generates an HTML
    # file with all the relevant information shown.

    # Create or overwrite the output file.
    output_file = open('index.html', 'w')

    # Retrieve HTML template from external file.
    content_file = open('template/template-main.html', 'r')
    content = content_file.read()

    # Replace the movie tiles' placeholder generated content.
    rendered_content = content.format(
        genre_list=create_genre_list_content(genres),
        movie_sections=create_movie_sections_content(movies, genres))

    # Save the newly generated file.
    output_file.write(rendered_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible).
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)


def getPosterImageURL(movie):
    # Returns a path to the requested movie's poster image.

    valid = "image/movies/" + movie.id + "/poster.png"
    invalid = "image/movies/0000 Unknown/poster.png"

    return valid if os.path.isfile(valid) else invalid


def getMovieBoxartImageURL(movie):
    # Returns a path to the requested movie's boxart image.

    valid = "image/movies/" + movie.id + "/boxart.png"
    invalid = "image/movies/0000 Unknown/boxart.png"

    return valid if os.path.isfile(valid) else invalid


def getMovieThumbnailImageURL(movie):
    # Returns a path to the requested movie's thumbnail image.

    valid = "image/movies/" + movie.id + "/thumbnail.png"
    invalid = "image/movies/0000 Unknown/thumbnail.png"

    return valid if os.path.isfile(valid) else invalid

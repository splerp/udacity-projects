import webbrowser
import os
import re

# A single movie entry html template
movie_tile_content = '''
<div class="col-lg-4 movie-tile text-center"
data-trailer-youtube-id="{trailer_youtube_id}"
data-toggle="modal"
data-target="#trailer">
	<img src="{poster_image_url}" width="220">
	<h2>{movie_title} ({release_date})</h2>
	<div class="shortdesc">{movie_short_desc}</div>
	<div class="longdesc">{movie_long_desc}</div>
</div>
'''

# Creates an HTML unordered list out of the available genres.
def create_genre_list_content(genres):
	
	to_return = '<ul>'
	
	g = "All"
	
	to_return += '<li data-genre="' + g + '">' + g + '</li>'
	
	for g in genres:
		to_return += '<li data-genre="' + g + '">' + g + '</li>'
	
	g = "Unknown"
	to_return += '<li data-genre="' + g + '">' + g + '</li>'
	
	to_return += '</ul>'
	return to_return

# Creates the beginning of a group of movies ("genre-section").
def begin_genre_content(genre):

	return '''
	<div id="genre-{genrename}" class="container genre-section">
	<h1>{genrename}</h1>
	'''.format(genrename=genre)
	
def end_genre_content():

	return "</div>"


def create_movie_sections_content(movies, genres):
	# The HTML content for this section of the page

	genre_contents = {}

	genre_contents["All"] = begin_genre_content("All")
	
	# set up initial genre content.
	for g in genres:
		genre_contents[g] = begin_genre_content(g)

	genre_contents["Unknown"] = begin_genre_content("Unknown")

	for movie in movies:

		# Extract the youtube ID from the url

		movie_content = movie_tile_content.format(
						movie_title=movie.title,
						release_date=movie.release_date.strftime('%Y'),
						poster_image_url=getPosterImageURL(movie),
						trailer_youtube_id=movie.trailer_youtube_id,
						movie_short_desc=movie.short_description,
						movie_long_desc=movie.long_description
					)

		# Search for the specified genre
		found = False
		for g in genres:
			if(movie.genre == g):
				# Append the tile for the movie with its content filled in
				genre_contents["All"] += movie_content
				genre_contents[g] += movie_content
				found = True
		
		# If not found, add to "unknown" category.
		if not found:
			genre_contents["All"] += movie_content
			genre_contents["Unknown"] += movie_content

	content = ''

	for key, value in genre_contents.items():
		#print("Adding content to the content..")
		value += end_genre_content()   
		content += value

	return content


def open_movies_page(movies, genres):
	# Create or overwrite the output file
	output_file = open('index.html', 'w')

	# Retrieve HTML template from external file.
	content_file = open('template/template-main.html', 'r')
	content = content_file.read()

	# Replace the movie tiles' placeholder generated content
	rendered_content = content.format(
		genre_list=create_genre_list_content(genres),
		movie_sections=create_movie_sections_content(movies, genres))

	# Output the file
	output_file.write(rendered_content)
	output_file.close()

	# open the output file in the browser (in a new tab, if possible)
	url = os.path.abspath(output_file.name)
	webbrowser.open('file://' + url, new=2)

# Each of these functions returns a path to the requested movie's image.
def getPosterImageURL(movie):

	return "image/movies/" + movie.id + "/poster.png"

def getMovieBoxartImageURL(movie):

	return "image/movies/" + movie.id + "/boxart.png"

def getMovieThumbnailImageURL(movie):

	return "image/movies/" + movie.id + "/thumbnail.png"








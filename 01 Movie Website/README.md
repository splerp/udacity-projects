# Project 1 - Movie Website
A collection of scripts that can generate a simple .html page that contains a list of movies.

## Installation
#### Prerequisites

To run the python scripts, a version of python 3.0 must be installed. [link](https://www.python.org/downloads/)

#### Running the script (Windows)

1. Clone this repository, or ownload `freshtomatoes.py`, `media.py` and `pagegenerator.py`.
2. Open command prompt to the directory they are located in.
3. run the command "py freshtomatoes.py"
4. A page should open displaying the newly generated webpage.

## Modifying the file generation

- All the movie information is stored in the freshtomatoes.py file.
- Each movie is an instance of the Movie class, appended to the "movies" list.

#### Modifying an existing movie's information

Find the relevant movie instance and update the required information. Re-run the script to generate the new file.

#### Adding a new movie

Using an existing movie for reference, create a new movie instance and append it to the "movies" list. Re-run the script to generate the new file.

## Movie images directory layout

When a movie is added to the movies list, the id field corresponds to the folder name in image/movies that contains that movie's images.

This folder should include `boxart.png`, `poster.png` and `thumbnail.png`.

A movie's ID is created from a unique number, followed by a space, then the movie's title condensed to only the letters and numbers.

## Code base

The content of `pagegenerator.py` was originally created by Udacity for the Full Stack Developer course. [link](https://github.com/adarsh0806/udacity-full-stack/tree/master/p1)

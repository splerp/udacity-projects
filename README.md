# udacity-projects
Repository of Udacity projects for the Full Stack Developer course.

# [Project 1: Movie Trailer Website](01 Movie Website/)
A collection of scripts that can generate a simple .html page that contains a list of movies.

# [Project 2: Tournament Results](02 Tournament Results/)
A collection of scripts to generate and test a database that stores players, tournaments, and each game players have participated in.

# [Project 3: Multi User Blog](03 Multi User Blog/)
Google App Engine implementation of a simple user blog.

## Installation
No installation required - visit the website here:
#### [udacity-blog-site.appspot.com](http://www.udacity-blog-site.appspot.com)

## Usage
#### Registering
1. From the main page, click on "Login here!".
2. From here, click the "Register here" link.
3. Choose a name and password, and specify an option email address.
4. Click the register button.

#### Logging In
1. From the main page, click on "Login here!".
2. Enter your username and password.
3. Click the Log In button.

#### Viewing a blog post
1. From the main page, click on any blog post title or image to view the contents.

#### Adding a blog post
1. On the main navigation panel, click "Create Post"
2. Choose a title and summary to appear in the blog list.
3. Optionally, choose a thumbnail image to display.
4. Write all the contents of the post in the Contents section.
5. Click the Post button.

#### Editing / Deleting a blog post
1. View the blog post listing.
2. Next to any blog post written by you, click the edit / delete links.

#### Liking / Disliking a blog post
1. View the blog post listing.
2. Next to any blog post written by somebody else, click the thumbs up / thumbs down buttons to increase / decrease that post's point count.

## Database Structure
The various data stored in the Google App Engine database is structured using these entities:

#### SiteUser
Stores information about a registered user.

#### BlogPost
Stores information about a blog post. Contains a reference to a SiteUser.

#### BlogPostReaction
Stores all 'reactions' to blog posts (i.e. likes and dislikes by users). Each entry contains a reference to the SiteUser that reacted and the BlogPost they reacted to.

#### BlogPostComment
Stores information about a blog post comment. Contains a reference to the SiteUser commenter and the BlogPost the comment is for.

## Code layout
- main.py: Entry point for program. Defines handlers for main pages of site and all routing information.

#### src/ folder
- data.py: Contains definitions for database models.
- route.py: Base Handler class is defined here.
- security.py: All functions that interact with cookies and validating users / passwords.
- validation.py: Functions that handler registration / login validation.

#### scripts/ folder
- Javascript files.


#### style/ folder
- CSS files.


#### templates/ folder
- Each file contains a separate jinja template. base.html defines the base page contents.

## Code base
The structure of this site is based on the content of the Full Stack Developer course by Udacity. [[link](https://github.com/adarsh0806/udacity-full-stack/tree/master/p2)]

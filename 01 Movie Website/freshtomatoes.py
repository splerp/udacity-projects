from datetime import date
from media import movie
import pagegenerator as gen

genres = ["Romance", "Action", "Thriller", "Drama", "Comedy"]
genres.sort()

movies = list()
movies.append(movie(
			id="0001 TheLionKing",
			title="The Lion King",
			rd=date(1994, 8, 25),
			genre="Action",
			vidid="4sj1MT05lAA",
			sdesc="A lion Hakuna Matatas",
			ldesc="Trouble in the pride as Simba massacres left right and centre.",
			))
			
movies.append(movie(
			id="0002 TheLionKing2ReturnoftheJedi",
			title="The Lion King 2 - Return of the Jedi",
			rd=date(1998, 10, 27),
			genre="Action",
			vidid="gYbW1F_c9eM",
			sdesc="The force.",
			ldesc="Simba uses the force (just kidding)",
			))
			
movies.append(movie(
			id="0003 StarRoarsMufasaStrikesBack",
			title="Star Roars - Mufasa Strikes Back",
			rd=date(2012, 6, 6),
			genre="Romance",
			vidid="4raW1agJG7U",
			sdesc="Mufasa decides enough is enough",
			ldesc="Trouble in the pride as Mufasa massacres left right and centre.",
			))
			
movies.append(movie(
			id="0004 Inception",
			title="Inception",
			rd=date(2010, 7, 22),
			genre="Thriller",
			vidid="8hP9D6kZseM",
			sdesc="",
			ldesc="",
			))
			
movies.append(movie(
			id="0005 HowToTrainYourDragon",
			title="How To Train Your Dragon",
			rd=date(2010, 3, 25),
			genre="Action",
			vidid="oKiYuIsPxYk",
			sdesc="",
			ldesc="",
			))
			
movies.append(movie(
			id="0006 BridgetoTerabithia",
			title="Bridge to Terabithia",
			rd=date(2007, 2, 16),
			genre="Drama",
			vidid="3SvqEIKP4t8",
			sdesc="",
			ldesc="",
			))
			
movies.append(movie(
			id="0007 ThePrincessBride",
			title="The Princess Bride",
			rd=date(1987, 12, 3),
			genre="Romance",
			vidid="njZBYfNpWoE",
			sdesc="",
			ldesc="",
			))
			
movies.append(movie(
			id="0008 Megamind",
			title="Megamind",
			rd=date(2010, 12, 9),
			genre="Comedy",
			vidid="NPI0eatlo_M",
			sdesc="",
			ldesc="",
			))
			
movies.append(movie(
			id="0009 Chronicle",
			title="Chronicle",
			rd=date(2012, 2, 2),
			genre="Thriller",
			vidid="UD0DshFbmxA",
			sdesc="",
			ldesc="",
			))

movies.append(movie(
			id="0010 TheCabinintheWoods",
			title="The Cabin in the Woods",
			rd=date(2011, 6, 14),
			genre="Thriller",
			vidid="OJUIgf7lsCY",
			sdesc="",
			ldesc="",
			))

movies.append(movie(
			id="0000 Unknown",
			title="Toy Story",
			rd=date(2011, 6, 14),
			genre="Comedy",
			vidid="OJUIgf7lsCY",
			sdesc="",
			ldesc="",
			))
			
movies.append(movie(
			id="0000 Unknown",
			title="Toy Story 2",
			rd=date(2011, 6, 14),
			genre="Comedy",
			vidid="OJUIgf7lsCY",
			sdesc="",
			ldesc="",
			))

movies.append(movie(
			id="0000 Unknown",
			title="Whiplash",
			rd=date(2011, 6, 14),
			genre="Drama",
			vidid="OJUIgf7lsCY",
			sdesc="",
			ldesc="",
			))

movies.append(movie(
			id="0000 Unknown",
			title="Looper",
			rd=date(2011, 6, 14),
			genre="Thriller",
			vidid="OJUIgf7lsCY",
			sdesc="",
			ldesc="",
			))

movies.append(movie(
			id="0000 Unknown",
			title="Gravity",
			rd=date(2011, 6, 14),
			genre="Thriller",
			vidid="OJUIgf7lsCY",
			sdesc="",
			ldesc="",
			))

movies.append(movie(
			id="0000 Unknown",
			title="Harry Potter and the Philosopher's Stone",
			rd=date(2011, 6, 14),
			genre="Drama",
			vidid="OJUIgf7lsCY",
			sdesc="",
			ldesc="",
			))

movies.append(movie(
			id="0000 Unknown",
			title="The Incredibles",
			rd=date(2011, 6, 14),
			genre="Action",
			vidid="OJUIgf7lsCY",
			sdesc="",
			ldesc="",
			))

movies.append(movie(
			id="0000 Unknown",
			title="The Lord of the Rings: The Two Towers",
			rd=date(2011, 6, 14),
			genre="Action",
			vidid="OJUIgf7lsCY",
			sdesc="",
			ldesc="",
			))

movies.append(movie(
			id="0000 Unknown",
			title="Chicken Run",
			rd=date(2011, 6, 14),
			genre="Comedy",
			vidid="OJUIgf7lsCY",
			sdesc="",
			ldesc="",
			))

movies.append(movie(
			id="0000 Unknown",
			title="Monety Python and the Holy Grail",
			rd=date(2011, 6, 14),
			genre="Comedy",
			vidid="OJUIgf7lsCY",
			sdesc="",
			ldesc="",
			))

movies.append(movie(
			id="0000 Unknown",
			title="101 Dalmations",
			rd=date(2011, 6, 14),
			genre="Comedy",
			vidid="OJUIgf7lsCY",
			sdesc="",
			ldesc="\"Uhhhh, so like, there's this family right? That's really nice and stuff. Anyawy, so they get the dogs right? Like the dude has a dalmation, and falls in love a girl who also has a dalmation. Then, 99 kids somehow (probably adopted) happen. Then this really evil person, Cruella de Vil, she just happens to find 101 of them. So what are you gonna do? You gotta hunt them down. But you can't because it's a Disney film. Then she dies, probably. Then they got a better house (like, the good people).\"",
			))

movies.append(movie(
			id="0000 Unknown",
			title="Up",
			rd=date(2011, 6, 14),
			genre="Action",
			vidid="OJUIgf7lsCY",
			sdesc="",
			ldesc="\"I don't really remember Up, to be honest. Only the balloons. Um... pff. What even happens in the story? He gets together with this girl, that he likes. She can't have kids, she dies, he's sad, steals a lot of balloons, attaches them to his house, runs away with his house, runs away from the police. Ends up on a mountain, with a dog, and a kid? Don't know where the kid came from, but um... dog dies, then doesn't die, kid doesn't die. Old guy isn't sad any more.\"",
			))


######
	
gen.open_movies_page(movies, genres)
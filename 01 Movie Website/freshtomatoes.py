from datetime import date
from media import Movie
import pagegenerator as gen

genres = ["Romance", "Action", "Thriller", "Drama", "Comedy"]
genres.sort()

movies = list()
movies.append(Movie(
            id="0001 TheLionKing",
            title="The Lion King",
            rd=date(1994, 8, 25),
            genre="Action",
            vidid="4sj1MT05lAA",
            sdesc="A lion Hakuna Matatas",
            ldesc="Trouble in the pride as Simba massacres"
            " left right and centre.",
            ))

movies.append(Movie(
            id="0002 TheLionKing2ReturnoftheJedi",
            title="The Lion King 2 - Return of the Jedi",
            rd=date(1998, 10, 27),
            genre="Action",
            vidid="gYbW1F_c9eM",
            sdesc="The force.",
            ldesc="Simba uses the force (just kidding)",
            ))

movies.append(Movie(
            id="0003 StarRoarsMufasaStrikesBack",
            title="Star Roars - Mufasa Strikes Back",
            rd=date(2012, 6, 6),
            genre="Romance",
            vidid="4raW1agJG7U",
            sdesc="Mufasa decides enough is enough",
            ldesc="Trouble in the pride as Mufasa"
            " massacres left right and centre.",
            ))

movies.append(Movie(
            id="0004 Inception",
            title="Inception",
            rd=date(2010, 7, 22),
            genre="Thriller",
            vidid="8hP9D6kZseM",
            ))

movies.append(Movie(
            id="0005 HowToTrainYourDragon",
            title="How To Train Your Dragon",
            rd=date(2010, 3, 25),
            genre="Action",
            vidid="oKiYuIsPxYk",
            ))

movies.append(Movie(
            id="0006 BridgetoTerabithia",
            title="Bridge to Terabithia",
            rd=date(2007, 2, 16),
            genre="Drama",
            vidid="3SvqEIKP4t8",
            ))

movies.append(Movie(
            id="0007 ThePrincessBride",
            title="The Princess Bride",
            rd=date(1987, 12, 3),
            genre="Romance",
            vidid="njZBYfNpWoE",
            ))

movies.append(Movie(
            id="0008 Megamind",
            title="Megamind",
            rd=date(2010, 12, 9),
            genre="Comedy",
            vidid="NPI0eatlo_M",
            ))

movies.append(Movie(
            id="0009 Chronicle",
            title="Chronicle",
            rd=date(2012, 2, 2),
            genre="Thriller",
            vidid="UD0DshFbmxA",
            ))

movies.append(Movie(
            id="0010 TheCabinintheWoods",
            title="The Cabin in the Woods",
            rd=date(2011, 6, 14),
            genre="Thriller",
            vidid="OJUIgf7lsCY",
            ))

movies.append(Movie(
            id="0011 ToyStory",
            title="Toy Story",
            rd=date(1995, 12, 7),
            genre="Comedy",
            vidid="4KPTXpQehio",
            ))

movies.append(Movie(
            id="0012 ToyStory2",
            title="Toy Story 2",
            rd=date(1999, 12, 2),
            genre="Comedy",
            vidid="Lu0sotERXhI",
            ))

movies.append(Movie(
            id="0013 Whiplash",
            title="Whiplash",
            rd=date(2015, 1, 8),
            genre="Drama",
            vidid="7d_jQycdQGo",
            ))

movies.append(Movie(
            id="0014 Looper",
            title="Looper",
            rd=date(2012, 9, 27),
            genre="Thriller",
            vidid="2iQuhsmtfHw",
            ))

movies.append(Movie(
            id="0015 Gravity",
            title="Gravity",
            rd=date(2013, 10, 3),
            genre="Thriller",
            vidid="OiTiKOy59o4",
            ))

movies.append(Movie(
            id="0016 HarryPotterandthePhilosophersStone",
            title="Harry Potter and the Philosopher's Stone",
            rd=date(2001, 11, 4),
            vidid="eKSB0gXl9dw",
            ))

movies.append(Movie(
            id="0017 TheIncredibles",
            title="The Incredibles",
            rd=date(2004, 12, 26),
            genre="Action",
            vidid="fwHlyurv-0U",
            ))

movies.append(Movie(
            id="0018 TheLordoftheRingsTheTwoTowers",
            title="The Lord of the Rings: The Two Towers",
            rd=date(2002, 12, 19),
            genre="Action",
            vidid="cvCktPUwkW0",
            ))

movies.append(Movie(
            id="0019 ChickenRun",
            title="Chicken Run",
            rd=date(2000, 12, 7),
            genre="Comedy",
            vidid="AEOfT7hUcDs",
            ))

movies.append(Movie(
            id="0020 MontyPythonandtheHolyGrail",
            title="Monty Python and the Holy Grail",
            rd=date(1975, 1, 1),
            genre="Comedy",
            vidid="LG1PlkURjxE",
            ))

movies.append(Movie(
            id="0021 OneHundredAndOneDalmations",
            title="One Hundred and One Dalmations",
            rd=date(1961, 1, 25),
            genre="Comedy",
            vidid="1Q_98VlWLF4",
            ldesc=("Uhhhh, so like, there's this family right? That's"
                   " really nice and stuff. Anyway, so they get the"
                   " dogs right?"
                   " Like the dude has a dalmation, and falls in love a girl"
                   " who also has a dalmation. Then, 99 kids somehow (probably"
                   " adopted) happen. Then this really evil person, Cruella"
                   " de Vil, she just happens to find 101 of them. So"
                   " what are you gonna"
                   " do? You gotta hunt them down. But you can't because it's"
                   " a Disney film. Then she dies, probably. Then they got a"
                   " better house (like, the good people).\""),
            ))

movies.append(Movie(
            id="0022 Up",
            title="Up",
            rd=date(2009, 9, 3),
            genre="Action",
            vidid="qas5lWp7_R0",
            ldesc=("I don't really remember Up, to be honest. Only"
                   " the balloons. Um... pff. What even happens in the story?"
                   " He gets together with this girl, that he likes."
                   " She can't have kids, she dies, he's sad, steals a lot of"
                   " balloons, attaches them to his house, runs away with his"
                   " house, runs away from the police. Ends up on a mountain,"
                   " with a dog, and a kid? Don't know where"
                   " the kid came from,"
                   " but um... dog dies, then doesn't die, kid doesn't die."
                   " Old guy isn't sad any more.\""),
            ))


def main():

    # Generate the webpage from this data.
    gen.open_movies_page(movies, genres)

if __name__ == '__main__':
    main()

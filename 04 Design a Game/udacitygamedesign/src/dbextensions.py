from google.appengine.ext import db

from src.data import SiteUser


def get_user_from_username(username):
    query = db.GqlQuery(
        ("SELECT * FROM SiteUser "
         "WHERE username = :1"), username.lower())

    # Retrieves first valid row, or None
    return query.get()


def get_rankings():
    rankings = []

    players = SiteUser.all()
    for player in players:

        wins = 0
        losses = 0
        for x in player.games:
            if x.game.game_state == 'complete':
                if x.is_winner:
                    wins += 1
                else:
                    losses += 1

        win_average = wins / (wins + losses) if (wins + losses) != 0 else 0

        rankings.append((player.username, wins, losses, win_average))

    # Sort by wins. If equal, breka ties with win frequency.
    # Sort by losses if both are equal (people with more
    # experience are ranked higher)
    rankings.sort(key=lambda tuple: (tuple[1], tuple[3], tuple[2]), reverse=True)
    
    return rankings
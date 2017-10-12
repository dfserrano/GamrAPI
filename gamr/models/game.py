from datetime import datetime

from gamr.models import db

class Game(db.Model):
    """
    Game object that access the datasource through SQLAlchemy
    For more information take a look at:
    http://flask-sqlalchemy.pocoo.org/2.3/quickstart/
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    year = db.Column(db.Integer)
    pic = db.Column(db.String(255))
    avgRating = db.Column(db.Float)
    votes = db.Column(db.Integer)

    def __init__(self, title, year, pic, avgRating, votes):
        """
        Initializes a Game object.
        @type  title: string
        @param title: The title of the game.
        @type  year: number
        @param year: The release year of the game.
        @type  pic: string
        @param pic: Link to the cover of the game.
        @type  avgRating: number
        @param avgRating: Average rating of the game.
        @type  votes: number
        @param votes: Number of votes for the game.
        """
        self.title = title
        self.year = year
        self.pic = pic
        self.avgRating = avgRating
        self.votes = votes

    def vote(self, rating):
        """
        Casts a vote with the given rating.
        @type  rating: number
        @param rating: The rating [0-1].
        """
        totalRating = self.avgRating * self.votes + rating
        newRating = totalRating / (self.votes + 1)

        self.avgRating = newRating
        self.votes = self.votes + 1

        db.session.commit()


    def __repr__(self):
        return '<Game ' + self.title + ' (' + str(self.year) + ') [' + str(self.avgRating) + '/' + str(self.votes) + ']>'

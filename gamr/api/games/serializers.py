from flask_restplus import fields
from gamr.api.restplus import api

# Game object used in endpoint responses
gameResponseModel = api.model('Game', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a game', example=1),
    'title': fields.String(required=True, description='Game title', example='Pac Man'),
    'year': fields.Integer(required=True, description='Release year of the game', example=1980),
    'pic': fields.String(required=True, description='Game picture', example='pacman.jpg'),
    'avgRating': fields.Float(required=True, description='Average rating of the game', example=0.87),
    'votes': fields.Integer(required=True, description='Number of votes for the game', example=23)
})

# Response wrapper for single games
singleGameResponseModel = api.inherit('Game response', {
    'data': fields.Nested(gameResponseModel)
})

# Response wrapper for list of games
listOfGamesResponseModel = api.inherit('Game response', {
    'data': fields.List(fields.Nested(gameResponseModel))
})

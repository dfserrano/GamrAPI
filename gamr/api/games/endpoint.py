import logging

from flask import request
from flask_restplus import Resource, abort
from sqlalchemy.sql import func
from flask_restplus import reqparse
from gamr.api.errors import InvalidInputError, NotFoundError
from gamr.api.games.serializers import singleGameResponseModel, listOfGamesResponseModel
from gamr.api.restplus import api
from gamr.models.game import Game

log = logging.getLogger(__name__)

# Creates namespace games/ for operations associated to games
ns = api.namespace('games', description='Operations related to games')

@ns.route('/top')
@api.response(400, 'Invalid n supplied')
@api.response(404, 'Games not found.')
class TopGames(Resource):

    @api.marshal_with(listOfGamesResponseModel)
    @api.param('n', 'Number of games to return', required=False, default=3, type=int, min=1, max=10)
    def get(self):
        """
        Top n games
        """
        parser = reqparse.RequestParser()
        parser.add_argument('n', required=False)
        args = parser.parse_args()

        n = 3
        try:
            n = int(args['n'])
        except:
            if args['n'] != None:
                raise InvalidInputError('The parameter n has to be an integer.')

        if n < 1 or n > 10:
            raise InvalidInputError('The parameter n has to be between 1 and 10.')

        topGames = Game.query.order_by(Game.avgRating.desc()).limit(n)

        return { 'data': topGames }

@ns.route('/random')
@api.response(404, 'Game not found.')
class RandomGame(Resource):

    @api.marshal_with(singleGameResponseModel)
    def get(self):
        """
        Random game
        """
        randomGame = Game.query.order_by(func.random()).first()

        if randomGame == None:
            raise NotFoundError('A random game could not be retrieved from our collection.')

        return { 'data': randomGame }


@ns.route('/<id>')
@api.response(400, 'Invalid ID supplied')
@api.response(404, 'Game not found.')
class GameItem(Resource):

    @api.marshal_with(singleGameResponseModel)
    def get(self, id):
        """
        Find game by ID
        """
        if not id.isdigit():
            raise InvalidInputError('The game ID has to be an integer.')

        game = Game.query.filter(Game.id == id).first()

        if game == None:
            raise NotFoundError('The game with ID ' + str(id) + ' is not in our collection.')

        return { 'data': game }


@ns.route('/<id>/vote')
@api.response(400, 'Invalid ID supplied')
@api.response(404, 'Game not found.')
class GameVote(Resource):

    @api.response(204, 'Vote successfully added.')
    @api.param('rating', 'Rating for the game', _in=u'formData', required=True, default=0, type=int, min=0, max=1)
    def put(self, id):
        """
        Vote for a game
        """
        parser = reqparse.RequestParser()
        parser.add_argument('rating', required=True)
        args = parser.parse_args()
        #todos[todo_id] = request.form['data']


        # Validation
        rating = 0
        try:
            rating = int(args['rating'])
        except:
            raise InvalidInputError('The rating has to be an integer.')

        if rating < 0 or rating > 1:
            raise InvalidInputError('The rating has to be 0 or 1.')

        if not id.isdigit():
            raise InvalidInputError('The game ID has to be an integer.')

        if not id.isdigit():
            raise InvalidInputError('The game ID has to be an integer.')

        game = Game.query.filter(Game.id == id).first()

        if game == None:
            raise NotFoundError('The game with ID ' + str(id) + ' is not in our collection.')

        # Vote
        game.vote(rating)

        return None, 204

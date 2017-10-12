from flask import Flask, Blueprint
from gamr.models import db
from gamr.api.restplus import api
from gamr.api.games.endpoint import ns as gamesNamespace
from gamr.models.game import Game
import unittest
import json

class TestGames(unittest.TestCase):
    """
    Test class for game-related operations.
    Note: The camelcase convention is changed in tests in order to use test discovery fetures.
    """

    def setUp(self):
        """
        Sets up the test application for each test case
        """
        app = Flask(__name__)

        # Test DB (different from the 'production' DB)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../test.sqlite'

        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False

        self.app = app.test_client()

        blueprint = Blueprint('api', __name__, url_prefix='/api')

        api.init_app(blueprint)
        api.add_namespace(gamesNamespace)

        app.register_blueprint(blueprint)
        db.init_app(app)


    def test_random(self):
        """
        Tests the API retrieves a random game, with all the attributes
        """
        print("\nRetrieving /api/games/random")
        response = self.app.get('/api/games/random')
        jsonResponse = json.loads(response.data)

        self.assertEqual(response.status_code, 200)

        self.assertIsNotNone(jsonResponse['data'])
        self.assertIsNotNone(jsonResponse['data']['id'])
        self.assertIsNotNone(jsonResponse['data']['title'])
        self.assertIsNotNone(jsonResponse['data']['year'])
        self.assertIsNotNone(jsonResponse['data']['avgRating'])
        self.assertIsNotNone(jsonResponse['data']['votes'])


    def test_top(self):
        """
        Tests the API retrieves the top games with default parameter
        """
        print("\nRetrieving /api/games/top")
        response = self.app.get('/api/games/top')
        jsonResponse = json.loads(response.data)

        self.assertEqual(response.status_code, 200)

        self.assertIsNotNone(jsonResponse['data'])
        self.assertEqual(len(jsonResponse['data']), 3)
        self.assertGreaterEqual(jsonResponse['data'][0]['avgRating'], jsonResponse['data'][1]['avgRating'])


    def test_top_with_parameter(self):
        """
        Tests the API retrieves the top games with custom parameter
        """
        print("\nRetrieving /api/games/top?n=2")
        response = self.app.get('/api/games/top?n=2')
        jsonResponse = json.loads(response.data)

        self.assertEqual(response.status_code, 200)

        self.assertIsNotNone(jsonResponse['data'])
        self.assertEqual(len(jsonResponse['data']), 2)
        self.assertGreaterEqual(jsonResponse['data'][0]['avgRating'], jsonResponse['data'][1]['avgRating'])


    def test_top_with_wrong_parameter(self):
        """
        Tests the API returns an error for top games with invalid parameter
        """
        print("\nRetrieving /api/games/top?n=-1")
        response = self.app.get('/api/games/top?n=-1')
        jsonResponse = json.loads(response.data)

        self.assertEqual(response.status_code, 404)


    def test_get(self):
        """
        Tests the API retrieves the game with the given ID
        """
        print("\nRetrieving /api/games/1")
        response = self.app.get('/api/games/1')
        jsonResponse = json.loads(response.data)

        self.assertEqual(response.status_code, 200)

        self.assertIsNotNone(jsonResponse['data'])
        self.assertEqual(jsonResponse['data']['id'], 1)
        self.assertEqual(jsonResponse['data']['title'], "Super Mario Bros.")


    def test_vote_up(self):
        """
        Tests the API casts an upvote for the specified game
        """
        print("\nVoting up /api/games/1/vote")

        # Get game attrs before voting
        response = self.app.get('/api/games/1')
        jsonResponse = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(jsonResponse['data'])
        self.assertEqual(jsonResponse['data']['id'], 1)

        curRating = jsonResponse['data']['avgRating']
        curVotes = jsonResponse['data']['votes']
        expectedRating = ((curRating * curVotes) + 1) / (curVotes + 1)

        # Vote
        response = self.app.put('/api/games/1/vote', data=dict(rating=1))

        self.assertEqual(response.status_code, 204)

        # Get game attrs after voting
        response = self.app.get('/api/games/1')
        jsonResponse = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(jsonResponse['data'])
        self.assertEqual(jsonResponse['data']['id'], 1)
        self.assertAlmostEqual(jsonResponse['data']['avgRating'], expectedRating)


    def test_vote_down(self):
        """
        Tests the API casts a downvote for the specified game
        """
        print("\nVoting down /api/games/1/vote")

        # Get game attrs before voting
        response = self.app.get('/api/games/1')
        jsonResponse = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(jsonResponse['data'])
        self.assertEqual(jsonResponse['data']['id'], 1)

        curRating = jsonResponse['data']['avgRating']
        curVotes = jsonResponse['data']['votes']
        expectedRating = (curRating * curVotes) / (curVotes + 1)

        # Vote
        response = self.app.put('/api/games/1/vote', data=dict(rating=0))

        self.assertEqual(response.status_code, 204)

        # Get game attrs after voting
        response = self.app.get('/api/games/1')
        jsonResponse = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(jsonResponse['data'])
        self.assertEqual(jsonResponse['data']['id'], 1)
        self.assertAlmostEqual(jsonResponse['data']['avgRating'], expectedRating)


    def test_vote_inexistent_game(self):
        """
        Tests the API returns an error when voting for an inexistent game
        """
        print("\nVoting inexistent game /api/games/100/vote")
        response = self.app.put('/api/games/100/vote', data=dict(rating=0))

        self.assertEqual(response.status_code, 404)


    def test_vote_wrong_rating(self):
        """
        Tests the API returns an error when using a wrong rating for voting
        """
        print("\nVoting wrong rating /api/games/1/vote")

        response = self.app.put('/api/games/1/vote', data=dict(rating=5))
        self.assertEqual(response.status_code, 404)

        response = self.app.put('/api/games/1/vote', data=dict(rating=-5))
        self.assertEqual(response.status_code, 404)

        response = self.app.put('/api/games/1/vote')
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()

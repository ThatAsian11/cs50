from unittest import TestCase
from .models import Watchlist
from helpers import Search, Trending, format_query

# Create your tests here.
class WatchlistTestCase(TestCase):
    def test_search(self):
        multi_search = Search.all_search('game of thrones')
        movie = Search.movie_find(299534)
        formatted = format_query(' game of thrones  ')
        self.assertEqual(multi_search['results'][0]['name'], "Game of Thrones")
        self.assertEqual(movie['title'], "Avengers: Endgame")
        self.assertEqual(formatted, "game+of+thrones")

    
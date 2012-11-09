import os
from os.path import dirname,abspath
import site
site.addsitedir(dirname(dirname(dirname(dirname(dirname(abspath(__file__)))))))

import unittest

from adsabs.app import create_app
from config import config

class SearchTestCase(unittest.TestCase):

    def setUp(self):
        config.TESTING = True
        app = create_app(config)
        self.app = app.test_client()

    def test_search_page(self):
        rv = self.app.get('/searchcompare/solr?q=foo')
        assert 'ADS 2.0 Basic Search' in rv.data
        
if __name__ == '__main__':
    unittest.main()
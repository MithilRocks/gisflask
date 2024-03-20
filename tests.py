import main
import json
import os
from unittest import mock, TestCase, main as unittest_main

class FlaskTestCase(TestCase):

    def setUp(self):
        self.app = main.app.test_client()
        self.app.testing = True 

    def test_tile_status_code(self):
        '''
        Test if the application returns 200 when a tile is found
        '''

        # sends HTTP GET request to the application
        result = self.app.get('/tile?zoom=10&col=501&row=684') 

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_tile_not_found_status_code(self):
        '''
        Test if the application returns 404 when a tile is not found
        '''

        # sends HTTP GET request to the application
        result = self.app.get('/tile?zoom=1&col=1&row=1')

        # assert the status code of the response
        self.assertEqual(result.status_code, 404) 

    def test_tile_no_params(self):
        '''
        Test if the application returns 400 when no parameters are provided
        '''

        # sends HTTP GET request to the application
        result = self.app.get('/tile') 

        # assert the status code of the response
        self.assertEqual(result.status_code, 400)
    
    @mock.patch.dict('os.environ', {'MBTILES': 'static/nonexistent.mbtiles'})
    def test_mbtiles_connection(self):
        '''
        Test if the application returns 500 when the mbtiles file is not found
        '''

        # sends HTTP GET request to the application
        result = self.app.get('/tile?zoom=10&col=501&row=684') 

        # assert the status code of the response
        self.assertEqual(result.status_code, 500)

        # Remove the nonexistent.mbtiles file after the test is done
        os.remove('static/nonexistent.mbtiles')
    
    @mock.patch.dict('os.environ', {'MBTILES': 'static/no_table.mbtiles'})
    def test_tile_table_not_found(self):
        '''
        Test if the application returns 500 when the tiles table is not found
        '''

        # sends HTTP GET request to the application
        result = self.app.get('/tile?zoom=10&col=501&row=684') 

        # assert the status code of the response
        self.assertEqual(result.status_code, 500)

if __name__ == '__main__':
    unittest_main()
import unittest
import boto3
import simplejson

from app import lambda_handler


class TestAPI(unittest.TestCase):
    def test_getApi_works(self):

        result = lambda_handler(0,0)
        self.assertEqual(result['statusCode'], 200)

if __name__ == '__main__':
    unittest.main()
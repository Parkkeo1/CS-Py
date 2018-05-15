import unittest
from src.server import *

class PostRequestsTest(unittest.TestCase):
    def setUp(self):
        cs_py.config['TESTING'] = True
        cs_py.config['WTF_CSRF_ENABLED'] = False
        cs_py.config['DEBUG'] = False

        self.test_cspy = cs_py.test_client()
        self.assertEqual(cs_py.debug, False)

    def tearDown(self):
        pass

    def test_empty_postrequest(self):
        response = self.test_cspy.post('/GS', data={})
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
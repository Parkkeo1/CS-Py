import unittest
import json
from src.flask_webapp import *

class PostRequestsTest(unittest.TestCase):

    def setUp(self):
        cs_py.config['DATABASE'] = 'tests/test_data.db'
        cs_py.config['TESTING'] = True
        cs_py.config['WTF_CSRF_ENABLED'] = False
        cs_py.config['DEBUG'] = False
        cs_py.config['STATE'] = True

        self.test_cspy = cs_py.test_client()
        self.assertEqual(cs_py.debug, False)

    @classmethod
    def setUpClass(cls):
        init_table_if_not_exists(cls.get_test_db())

    def tearDown(self):
        self.get_test_db().cursor().execute('DELETE FROM per_round_data')

    # ---------------------------

    @classmethod
    def get_test_db(cls):
        return sqlite3.connect('tests/test_data.db')

    @classmethod
    def get_db_as_df(cls):
        return pd.read_sql('SELECT * FROM per_round_data', cls.get_test_db())

    # ---------------------------

    def test_empty_postrequest(self):
        response = self.test_cspy.post('/GS', data={})
        self.assertEqual(response.status_code, 200)

    def test_endround_entry(self):
        self.test_cspy.post('/GS', json=json.load(open('tests/endround_data.json')),
                                   headers={'content-type': 'application/json'})
        result_df = self.get_db_as_df()
        self.assertEqual(1, len(result_df.index))
        self.assertEqual(1515881032, result_df.iloc[0]['Time'])

if __name__ == "__main__":
    unittest.main()
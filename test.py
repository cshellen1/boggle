from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):

    def setUp(self):
            """Stuff to do before every test."""
            self.client = app.test_client()
    
    
    def test_root(self):
        """make sure HTML is displayed and game board is in the session"""
        
        with self.client:
            resp = self.client.get('/')
            html = resp.get_data(as_text=True)
            self.assertIn('board', session)
            self.assertIn('<form method="POST">', html)
            self.assertIn('<table id="board">', html)
            self.assertEqual(resp.status_code, 200)
            
    def test_word_form(self):
        """make sure user submitted word is validated"""
        
        with self.client as client:
            with client.session_transaction() as session:
                session['board'] = [["B", "L", "U", "E", "S"], 
                                    ["B", "L", "U", "E", "S"], 
                                    ["B", "L", "U", "E", "S"], 
                                    ["B", "L", "U", "E", "S"], 
                                    ["B", "L", "U", "E", "S"]]
                                            
        resp = self.client.get('/check-word?word=blue')
        self.assertTrue(resp.json['result'] == 'ok')
        self.assertTrue(resp.status_code == 200)
          
    def test_score_nplays_update(self):
        """test that the session is updated with new high score and number of times played"""

        with self.client as client:
            # with client.session_transaction() as session:
            #     session['nplays'] = 5
            #     session['high_score'] = 5
            resp = self.client.post('/update-score-plays', json={"score": 22})
            self.assertEqual(resp.status_code, 200)   
            self.assertEqual(session['high_score'], 22)
            self.assertEqual(session['nplays'], 1)
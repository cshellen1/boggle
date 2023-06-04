from flask import Flask, session, request, render_template, jsonify
from boggle import Boggle

from flask_debugtoolbar import DebugToolbarExtension

boggle_game = Boggle()

app = Flask(__name__)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = 'chickensarecool12345678'
debug = DebugToolbarExtension(app)


@app.route('/')
def display_board():
    """create and display newly generated board"""
    board = boggle_game.make_board()
    session['board'] = board
    return render_template('board.html')
    
@app.route('/check-word')
def check_word():
    """check user input word for validity"""
    word = request.args['word']
    response = boggle_game.check_valid_word(session['board'], word)
    return jsonify({'result': response})
    
@app.route('/update-score-plays', methods = ['POST'])
def update_score_plays():
    """ update the current users high score and the number of times played. send response back to script.js"""
    score = request.json['score']
    highscore = session.get('high_score', 0)
    nplays = session.get('nplays', 0)
    
    session['high_score'] = max(score, highscore)
    session['nplays'] = nplays + 1
    return jsonify(brokeRecord=score > highscore) 
from boggle import Boggle
from flask  import Flask, request, render_template, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension

app = FLASK(__name__)
app.config["SECRET_KEY"] = "abc123uandmeGurl"

boggle_game = Boggle()

@app.route("/")
def homepage():
    """Show Board."""

    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    cplays = session.get("cplays", 0)

    return render_template("index.html", board=board, highscore=highscore, cplays=cplays)


@app.route("/check-word")
def check_word():
    """Check if word is in dictionary."""

    word = request.args["word"]
    board = session["board"]
    decision = boggle_game.check_valid_word(board, word)

    return jsonify({'result': decision})

@app.route("/post-score", methods=["POST"])
def post_score():
    """Take in score, recieve num of plays, and update highscore if beaten."""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    cplays = session.get("cplays", 0)

    session['cplays'] = cplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)
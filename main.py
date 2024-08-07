from flask import Flask
from Game import Game


game = Game()


app = Flask(__name__)

@app.route("/")
def index():
    game.play()

app.run(host = "127.0.0.1", port = 8080, debug = True)
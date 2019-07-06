from flask import Flask, render_template
from games.blueprint_games import games_b

app = Flask(__name__)
app.register_blueprint(games_b)

@app.route('/')
def hi():
    return 'Hi'

if __name__ == '__main__':
    app.run(debug=True)

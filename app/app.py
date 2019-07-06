from flask import Flask

app = Flask(__name__)

@app.route('/')
def hi():
    return 'Hi'

@app.route('/sign-up')
def sign_up():
    return 'Sign up'

@app.route('/login', methods=['GET', 'POST'])
def login():
    return 'Login (Get - form | Post - create user)'

@app.route('/game', methods=['GET', 'POST', 'DELETE'])
def game_create():
    return 'Game (Get -form | Post - create logic | Delete - delete logic)'

if __name__ == '__main__':
    app.run(debug=True)

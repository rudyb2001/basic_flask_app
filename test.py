from flask import Flask
import json

app = Flask(__name__)
@app.route("/")
def base():
    message = {"message": "Hello"}
    return json.dumps(message)

# Route with optional parameter
@app.route('/greet/', defaults={'name': 'Guest'})
@app.route('/greet/<name>')
def greet(name):
    return f'Hello, {name}!'

if __name__ == '__main__':
    app.run()
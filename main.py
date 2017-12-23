from flask import Flask, request, render_template, session
from run import check_payload, parse_payload
import pandas as pd
import pprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'half-life 3 confirmed'


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/GS', methods=['POST'])
def GSHandler():
    if request.is_json:
        payload = request.get_json()
        if check_payload(payload):
            print(parse_payload(payload))

    return 'JSON Posted'


if __name__ == "__main__":
    app.run(debug=True)

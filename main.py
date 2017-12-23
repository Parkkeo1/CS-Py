from flask import Flask, request, render_template, session
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'half-life 3 confirmed'


@app.route('/', methods=['GET', 'POST'])
def receiver():
    if request.is_json:
        payload = request.get_json()
        content = json.loads(payload)
        return content


if __name__ == "__main__":
    app.run(debug=True)
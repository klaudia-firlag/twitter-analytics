from flask import Flask

app = Flask(__name__)


@app.route("/")
def twitter_analytics():
    html = "<h3>Twitter Analytics APP</h3>"
    return html


if __name__ == "__main__":
    app.run(host='localhost', port=80)

from flask import Flask, render_template, session

from auth.auth import auth
from settings import (
    FLASK_SECRET_KEY,
    DATABASE_HOST,
    DATABASE_PASSWORD,
    DATABASE_USER,
    DATABASE,
)

app = Flask(__name__)


app.config.from_mapping(
    SECRET_KEY=FLASK_SECRET_KEY,
    DATABASE_HOST=DATABASE_HOST,
    DATABASE_PASSWORD=DATABASE_PASSWORD,
    DATABASE_USER=DATABASE_USER,
    DATABASE=DATABASE,
)

app.secret_key = FLASK_SECRET_KEY

app.register_blueprint(auth)


@app.route("/", methods=["GET"])
def main():
    logged_in = session.get("email")

    return render_template("index.html", logged_in=logged_in)


if __name__ == "__main__":
    app.run()

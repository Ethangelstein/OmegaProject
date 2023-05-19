import os

from flask import Flask, render_template

from auth.auth import auth

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY="mikey",
    DATABASE_HOST=os.environ.get("FLASK_DATABASE_HOST"),
    DATABASE_PASSWORD=os.environ.get("FLASK_DATABASE_PASSWORD"),
    DATABASE_USER=os.environ.get("FLASK_DATABASE_USER"),
    DATABASE=os.environ.get("FLASK_DATABASE"),
)

app.register_blueprint(auth)


@app.route("/", methods=["GET"])
def main():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()

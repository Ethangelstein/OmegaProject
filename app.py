import re
from flask import Flask, request, url_for, redirect, abort, render_template
import hashlib
from database.database import database

app = Flask(__name__)

db = database.connect()

cursor = db.cursor(
    dictionary=True,
)


@app.route("/", methods=["GET"])
def main():
    cursor.execute("select * from user")
    users = cursor.fetchall()

    return render_template("index.html", users=users)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Checks
        if is_password_incorrect(password):
            password_length = len(password)
            MIN_PASSWORD_LENGTH = 8
            reason = "menor" if password_length < MIN_PASSWORD_LENGTH else "mayor"

            return throwErrorTemplate(
                field="Password", reason=reason, value=MIN_PASSWORD_LENGTH
            )

        if not is_valid_email(email):
            return throwErrorTemplate(field="Email", reason="igual", value=email)

        sql = "insert into user (username, email, password) values(%s, %s, %s)"

        # Hash password
        salt = "NJOXSA?!#"

        # Concatenar la contraseña y la salt
        salted_password = password.encode("utf-8") + salt.encode("utf-8")

        # Calcular el hash SHA256 de la contraseña y la salt
        hashed_password = hashlib.sha256(salted_password).hexdigest()

        values = (username, email, hashed_password)
        cursor.execute(sql, values)
        midb.commit()

        return redirect(url_for("index"))
    return render_template("signup.html")


def is_password_incorrect(password):
    return len(password) <= 8 or len(password) >= 50


def is_valid_email(email):
    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(regex, email))


def throwErrorTemplate(field, reason, value):
    return render_template("error.html", field=field, reason=reason, value=value)


@app.route("/")
def index():
    return "Live :D"


if __name__ == "__main__":
    app.run()

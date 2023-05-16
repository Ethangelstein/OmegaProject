import re
from flask import Flask, request, url_for, redirect, abort, render_template
import hashlib

app = Flask(__name__)

import mysql.connector

midb = mysql.connector.connect(
    host="localhost", user="root", password="mysql", database="omega"
)

cursor = midb.cursor(
    dictionary=True,
)


@app.route("/", methods=["GET"])
def main():
    cursor.execute("select * from user")
    users = cursor.fetchall()
    # abort(403)
    # return redirect(url_for('Salame', post_id=2))
    # print(request.form)
    # print(request.form['llave1'])
    # print(request.form['llave2'])
    # return render_template('Cheese.html')

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


# -------------------------------------------------------------------------------------------


@app.route("/")
def index():
    return "Live :D"


@app.route("/Home", methods=["GET"])
def home():
    return render_template("Home.html", mensaje="Hola Mundo")


# GET, POST, PUT, PATCH, DELETE
@app.route("/post/<post_id>", methods=["GET", "POST"])
def Salame(post_id):
    if request.method == "GET":
        return "El id del post es " + post_id
    else:
        return "Este es otro metodo y no GET"


if __name__ == "__main__":
    app.run()

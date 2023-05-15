import re
from flask import Flask, request, url_for, redirect, abort, render_template

app = Flask(__name__)

import mysql.connector

midb = mysql.connector.connect(
    host="localhost", user="EthanG", password="eThñ921723%&", database="prueba"
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
        print(request.form)
        username = request.form["username"]
        email = request.form["email"]
        age = int(request.form["age"])

        # Checks
        if is_age_incorrect(age):
            reason = "menor" if age <= 0 else "mayor"

            return throwErrorTemplate(field="Age", reason=reason, value=age)

        if not is_valid_email(email):
            return throwErrorTemplate(field="Email", reason="igual", value=email)

        sql = "insert into user (username, email, age) values(%s, %s, %s)"

        values = (username, email, age)
        cursor.execute(sql, values)
        midb.commit()

        return redirect(url_for("index"))
    return render_template("signup.html")


def is_age_incorrect(age):
    return age <= 0 or age >= 100


def is_valid_email(email):
    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(regex, email))


def throwErrorTemplate(field, reason, value):
    return render_template("error.html", field=field, reason=reason, value=value)


# -------------------------------------------------------------------------------------------


@app.route("/")
def index():
    return "Hola Mundo"


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
    app.run(host="192.168.0.66", port=5000)

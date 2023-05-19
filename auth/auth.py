import hashlib
from flask import (
    Blueprint,
    flash,
    g,
    render_template,
    request,
    url_for,
    session,
    redirect,
)

from database.database import get_db

auth = Blueprint("auth", __name__, url_prefix="/auth")

from .utils import is_password_incorrect, is_valid_email
from utils import throwErrorTemplate


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        form = request.form

        username = form.get("username")
        email = form.get("email")
        password = form.get("password")

        database, cursor = get_db()

        if not username:
            return throwErrorTemplate(field="Username", reason="igual", value=username)

        sql = "select * from user where email = %s"

        cursor.execute(sql, [email])

        found_users_emails = [user.get("email") for user in cursor.fetchall()]

        if email in found_users_emails:
            return throwErrorTemplate(field="Email", reason="igual", value=email)

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
        database.commit()

        return redirect(url_for("main"))
    return render_template("signup.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db, c = get_db()
        error = None
        c.execute("select * from user where username = %s", (username,))
        user = c.fetchone()

        if user is None:
            error = "Usuario y/o contraseña inválida"
        elif not check_password_hash(user, ["password"], password):
            error = "Usuario y/o contrasela inválida"

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("login.html")

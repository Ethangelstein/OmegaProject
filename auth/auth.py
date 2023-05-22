from flask import (
    Blueprint,
    render_template,
    request,
    url_for,
    session,
    redirect,
)

from utils import throw_error_template
from database.database import get_db
from .utils import is_password_incorrect, is_valid_email, hash_password


auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        form = request.form

        username = form.get("username")
        email = form.get("email")
        password = form.get("password")

        try:
            database, cursor = get_db()
        except BaseException as error:
            return throw_error_template(f"Server Error: {error}")

        if not username:
            return throw_error_template("El username tiene que estar completo")

        sql = "select * from user where email = %s"

        cursor.execute(sql, [email])

        found_users_emails = [user.get("email") for user in cursor.fetchall()]

        if email in found_users_emails:
            return throw_error_template(f"El email {email} ya está en uso")

        # Checks
        if is_password_incorrect(password):
            MIN_PASSWORD_LENGTH = 8

            return throw_error_template(
                f"La contraseña tiene que ser mayor a {MIN_PASSWORD_LENGTH} caracteres"
            )

        if not is_valid_email(email):
            return throw_error_template(f"El email {email} es invalido")

        sql = "insert into user (username, email, password) values(%s, %s, %s)"

        hashed_password = hash_password(password)

        values = (username, email, hashed_password)
        cursor.execute(sql, values)
        database.commit()

        session["email"] = email

        return redirect(url_for("main"))
    return render_template("signup.html")

from flask import render_template


def throw_error_template(message="Error inesperado"):
    return render_template("error.html", message=message)

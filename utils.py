from flask import render_template


def throwErrorTemplate(message="Error inesperado"):
    return render_template("error.html", message=message)

from flask import render_template


def throwErrorTemplate(field, reason, value):
    return render_template("error.html", field=field, reason=reason, value=value)

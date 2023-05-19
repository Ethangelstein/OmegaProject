import mysql.connector
import click

from flask import current_app, g as context
from flask.cli import with_appcontext
from .schema import instructions


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("DB initialized")


def init_db():
    database, cursor = get_db()
    for i in instructions:
        cursor.execute(i)
    database.commit()


def get_db():
    try:
        if "database" not in context:
            context.database = mysql.connector.connect(
                host=current_app.config["DATABASE_HOST"],
                user=current_app.config["DATABASE_USER"],
                password=current_app.config["DATABASE_PASSWORD"],
                database=current_app.config["DATABASE"],
            )

            context.cursor = context.database.cursor(dictionary=True)

        return context.database, context.cursor

    except BaseException as error:
        print("Couldn't connect to MySQL DB")
        exit(1)

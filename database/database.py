import time
import click
import mysql.connector

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
    max_attempts = 3
    sleep_duration = 1  # Sleep for 1 second before each retry

    for attempt in range(1, max_attempts + 1):
        try:
            if "database" not in context:
                context.database = mysql.connector.connect(
                    host=current_app.config.get("DATABASE_HOST"),
                    user=current_app.config.get("DATABASE_USER"),
                    password=current_app.config.get("DATABASE_PASSWORD"),
                    database=current_app.config.get("DATABASE"),
                )

                context.cursor = context.database.cursor(dictionary=True)

            return context.database, context.cursor

        except mysql.connector.Error as error:
            print("Attempt", attempt, "- Couldn't connect to MySQL DB:", error)
            if attempt < max_attempts:
                print("Retrying in", sleep_duration, "seconds...")
                time.sleep(sleep_duration)

    print("Failed to connect to MySQL DB after", max_attempts, "attempts")
    exit(1)

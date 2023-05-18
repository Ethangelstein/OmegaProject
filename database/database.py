import mysql.connector
import click

from flask import current_app, g as context
from flask.cli import with_appcontext
from schema import instructions


class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        try:
            database = mysql.connector.connect(
                host=current_app.config["DATABASE_HOST"],
                user=current_app.config["DATABASE_USER"],
                password=current_app.config["DATABASE_PASSWORD"],
                database=current_app.config["DATABASE"],
            )

            return database
        except BaseException as error:
            print("Couldn't connect to MySQL DB")
            exit(1)

    def init_app(app):
        app.teardown_appcontext(close_db)
        app.cli.add_command(init_db_command)

    @click.command("init-db")
    @with_appcontext
    def init_db_command():
        init_db()
        click.echo("Base de datos inicializada")

    def init_db():
        db, c = get_db()
        for i in instructions:
            c.execute(i)

        db.commit()


database = Database("localhost", "root", "eThñ921723%&", "omega")

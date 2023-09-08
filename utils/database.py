from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

import click
import os

from flask.cli import with_appcontext

db = None

def open_db(url):
    db_engine = create_engine(url)
    global db
    db = scoped_session(sessionmaker(bind=db_engine))
    
    
def get_db():
    global db
    return db

    
def init_db():
    engine = create_engine(os.getenv("DATABASE_URL"))

    with engine.connect() as connection:
        with open("schema.sql") as schema:
            queries = schema.read().split(';')
            
            for query in queries:
                query = query.replace("\n", "")
                connection.execute(text(query))
                connection.commit()
        
    
@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Database was successfully initialized!")
    

def init_app(app):
    app.cli.add_command(init_db_command)
    
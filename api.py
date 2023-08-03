#api.py
from flask import Flask
import sqlite3
from flask_restful import Resource, Api

DATABASE = 'todolist.db'

app = Flask(__name__)
app.config.from_object(__name__)
api = Api(app)


# Define the API resource for getting the to-do list items
class ToDoListResource(Resource):
    def get(self):
        db = get_db()
        cur = db.execute('SELECT what_to_do, due_date, status FROM entries')
        entries = cur.fetchall()
        tdlist = [dict(what_to_do=row[0], due_date=row[1], status=row[2]) for row in entries]
        return tdlist


api.add_resource(ToDoListResource, '/api/items')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(app.config['DATABASE'])
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

if __name__ == "__main__":
    # Print all available routes in the Flask app
    print(app.url_map)


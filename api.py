from flask import Flask, render_template, redirect, g, request, url_for, jsonify, Response
import sqlite3
import urllib
import json

DATABASE = 'todolist.db'

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/api/items", methods=['GET'])
def get_items():
    db = get_db()
    cur = db.execute('SELECT what_to_do, due_date, status FROM entries')
    entries = cur.fetchall()
    tdlist = [dict(what_to_do=row[0], due_date=row[1], status=row[2])
              for row in entries]
    response = Response(json.dumps(tdlist), mimetype='application/json')
    return response


@app.route("/api/items", methods=['POST'])
def add_item():
    data = request.get_json()
    if not data or 'what_to_do' not in data or 'due_date' not in data:
        return jsonify({"error": "Missing data"}), 400

    db = get_db()
    db.execute('INSERT INTO entries (what_to_do, due_date) VALUES (?, ?)',
               [data['what_to_do'], data['due_date']])
    db.commit()
    return jsonify({"result": True}), 201


@app.route("/api/items/<item>", methods=['DELETE'])
def delete_item(item):
    db = get_db()
    db.execute('DELETE FROM entries WHERE what_to_do = ?', [item])
    db.commit()
    return jsonify({"result": True})


@app.route("/api/items/<item>", methods=['PUT'])
def update_item(item):
    db = get_db()
    db.execute('UPDATE entries SET status = ? WHERE what_to_do = ?', ['Done', item])
    db.commit()
    return jsonify({"result": True})


def get_db():
    """Opens a new database connection if there is none yet for the current application context."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(app.config['DATABASE'])
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


if __name__ == "__main__":
    app.run("0.0.0.0", port=5001)

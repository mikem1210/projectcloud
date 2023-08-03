from flask import Flask, render_template, redirect, g, request, url_for, jsonify, json
import urllib
import requests
import os

app = Flask(__name__)
# make sure to replace localhost with the actual IP of the backend service after you deploy the backend service on Google Cloud
# for example, like this: TODO_API_URL = "http://123.456.789.123:5001"
TODO_API_URL = "http://localhost:5001"


@app.route("/")
def show_list():
    try:
        resp = requests.get(TODO_API_URL + "/api/items")
        resp.raise_for_status()  # Check for any errors in the response
        resp_data = resp.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        resp_data = []

    return render_template('index.html', todolist=resp_data)


@app.route("/add", methods=['POST'])
def add_entry():
    what_to_do = request.form['what_to_do']
    due_date = request.form['due_date']
    try:
        requests.post(TODO_API_URL + "/api/items", json={"what_to_do": what_to_do, "due_date": due_date})
    except requests.exceptions.RequestException as e:
        print(f"Error adding item via API: {e}")
    
    return redirect(url_for('show_list'))


@app.route("/delete/<item>")
def delete_entry(item):
    item = urllib.parse.quote(item)  # this takes care of spaces in the item
    try:
        requests.delete(TODO_API_URL + f"/api/items/{item}")
    except requests.exceptions.RequestException as e:
        print(f"Error deleting item via API: {e}")

    return redirect(url_for('show_list'))


@app.route("/mark/<item>")
def mark_as_done(item):
    item = urllib.parse.quote(item)  # this takes care of spaces in the item
    try:
        requests.put(TODO_API_URL + f"/api/items/{item}")
    except requests.exceptions.RequestException as e:
        print(f"Error updating item status via API: {e}")

    return redirect(url_for('show_list'))


if __name__ == "__main__":
    app.run("0.0.0.0")

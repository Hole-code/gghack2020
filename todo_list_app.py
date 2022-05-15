from flask import Flask, render_template, redirect, url_for, request

from db import DataBase

import time
import datetime


db = DataBase("mongodb://localhost:27017", "ToDo_List")

app = Flask(__name__)


@app.route("/")
def task_lists():
    return redirect(url_for("tasklist_route"))


@app.route("/tasklist")
def tasklist_route():
    return render_template("tasklists.html", tasklists=db.get_tasklist())


@app.route("/tasklist/edit/<string:tasklist_id>", methods=["POST" , "GET"])
def tasklist_edit_route(tasklist_id: str):
    if request.method == "GET":
        return render_template("edit_name.html")

    tasklist = db.get_tasklist(tasklist_id=tasklist_id)
    tasklist["name"] = request.form["name"]
    tasklist["last_updated"] = datetime.datetime.now().isoformat()

    return redirect(url_for("tasklist_route"))


@app.route("/tasklist/delete/<string:tasklist_id>")
def tasklist_delete_route(tasklist_id: str):
    db.delete_tasklist(tasklist_id=tasklist_id)
    return redirect(url_for("tasklist_route"))


@app.route("/tasklist/create", methods=["GET","POST"])
def tasklist_create_route():
    if request.method == "GET":
        return render_template("create_tasklist.html")

    last_updated = datetime.datetime.now().isoformat()
    created_at = last_updated

    db.add_tasklist(name=request.form["name"], last_updated=last_updated, created_at=created_at)

    return redirect(url_for("tasklist_route"))


@app.route("/tasks/<string:tasklist_id>")
def tasks_route(tasklist_id: str):
    tasks = db.get_task(tasklist_id=tasklist_id)
    return render_template("tasks.html", tasks=tasks or [], tasklist_id=tasklist_id)


@app.route("/task/edit/<string:task_id>", methods=["POST" , "GET"])
def task_edit_route(task_id: str):
    if request.method == "GET":
        return render_template("edit_task.html")

    new_status = request.form["status"]
    last_updated = datetime.datetime.now().isoformat()
    name = request.form["name"]
    description = request.form["description"]        

    task = db.get_task(task_id=task_id)
    task["name"] = name
    task["description"] = description
    task["last_updated"] = last_updated
    task["status"] = new_status

    return redirect(url_for("tasks_route", tasklist_id=str(task["tasklist_id"])))


@app.route("/task/delete/<string:task_id>")
def delete_task(task_id: str):
    task = db.get_task(task_id=task_id)
    db.delete_task(task_id=task_id)

    return redirect(url_for("tasks_route", tasklist_id=str(task["tasklist_id"])))


@app.route("/task/create/<string:tasklist_id>", methods=["POST" , "GET"])
def create_task(tasklist_id: str):
    if request.method == "GET":
        return render_template("create_task.html", Priority=Priority)

    priority = request.form["priority"] 
    last_updated = datetime.datetime.now().isoformat()
    created_at = last_updated
    name = request.form["name"]
    description = request.form["description"]

    db.add_task(name=name, last_updated=last_updated, created_at=created_at, status=Status.NEW, priority=priority, description=description, tasklist_id=tasklist_id)

    return redirect(url_for("tasks_route", tasklist_id=tasklist_id))


if __name__ == "__main__":
    app.run(debug=True)

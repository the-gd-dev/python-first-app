from datetime import datetime

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    todo_date = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


# get all task
"""
1. validate if the request is a get or post.
2. if it's POST add task to db and  redirect to '/'.
3. else get all task and redirect to '/'
"""


@app.route('/', methods=["GET", "POST"])
def root():
    if request.method == "POST":
        print(request.form)
        task_title = request.form['task_title']
        task_description = request.form['task_description']
        task_date = request.form['task_date']
        new_task = Todo(title=task_title, description=task_description, todo_date=task_date)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue.'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("create.html", tasks=tasks)


# delete created task
"""
1. validate id if it exist in db.
2. if it's not in db return 404
3. else delete the todo task and redirect to '/'
"""


@app.route('/delete', methods=["POST"])
def delete_task():
    task_to_delete = Todo.query.get_or_404(request.form['id'])
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "Some issue occurred! while deleting task!"


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_task(id):
    find_task = Todo.query.get_or_404(id)
    if not find_task:
        return "404 Error."
    if request.method == "POST":
        try:
            find_task.title = request.form['task_title']
            find_task.description = request.form['task_description']
            find_task.todo_date = request.form['task_date']
            db.session.commit()
            return redirect('/')
        except:
            return "Some issue while updating data please try again."
    else:
        return render_template("update.html", task=find_task)


@app.route('/login', methods=["POST", "GET"])
def login():
    return render_template('login.html')


@app.route('/register', methods=["POST", "GET"])
def register():
    return render_template('register.html')


with app.app_context():
    db.create_all()
    db.session.commit()

app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)


@app.route('/')
def index():
    todo_list = Todo.query.all()
    return render_template('index.html', todo_list=todo_list)


@app.route('/add', methods=['POST'])
def add():
    text = request.form.get('text')
    new_todo = Todo(text=text, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/complete/<id>')
def complete(id):
    todo = Todo.query.get(id)
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    todo = Todo.query.get(id)
    if request.method == 'POST':
        todo.text = request.form.get('text')
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('update.html', todo=todo)


@app.route('/delete/<id>')
def delete(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

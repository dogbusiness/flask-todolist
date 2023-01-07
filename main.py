from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList
from wtforms.validators import DataRequired
import os
import string
import random
from datetime import datetime as dt

# Id generator for list ids
def id_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# Bootsrap Initialisation #
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Bootstrap(app)

# SQLAlchemy #
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///list-task.db'
with app.app_context():
    db = SQLAlchemy(app)
    # Uncomment to create db
    db.create_all() 
    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Task(db.Model):
    __tablename__ = "task"
    taskid = db.Column(db.Integer, primary_key=True)
    listid = db.Column(db.Integer, db.ForeignKey("list.listid"), nullable=False)
    description = db.Column(db.String(300))
    done = db.Column(db.Integer, nullable=False)

class List(db.Model):
    __tablename__ = "list"
    listid = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(200))
    listids = db.relationship('Task', backref='task')

# WTForms #
class SearchList(FlaskForm):
    list_id = StringField("ListID", validators=[DataRequired()], render_kw={"placeholder": "Search List by ID"})
    submit1 = SubmitField("Search")

class CreateNewList(FlaskForm):
    description = StringField("Write your task here.", validators=[DataRequired()], render_kw={"placeholder": "Enter your first task and press enter to save..."})
    submit2 = SubmitField("Submit")

class AddTask(FlaskForm):
    description = StringField("Write your task here.", validators=[DataRequired()], render_kw={"placeholder": "Write your task here."})
    submit3 = SubmitField("Submit")

class EditListName(FlaskForm):
    name = StringField('List Name', validators=[DataRequired()])
    submit4 = SubmitField("Submit")

edit_task_field = StringField("Edit Task", validators=[DataRequired()])
class EditTask(FlaskForm):
    description = FieldList(edit_task_field)
    submit5 = SubmitField("Submit")

# Pages #
@app.route('/search', methods=["POST"])
def search_list():
    search_form = SearchList()
    if search_form.validate_on_submit():
        print(search_form.list_id.data)
        return redirect(url_for('show_list', list_url=search_form.list_id.data))

@app.route('/new', methods=["POST", "GET"])
def new_list():
    search_form = SearchList()
    new_list_form = CreateNewList()
    new_list_created = False
    new_list_url = None
    if search_form.validate_on_submit():
        print(search_form.list_id.data)
        return redirect(url_for('show_list', list_url=search_form.list_id.data))
    if new_list_form.validate_on_submit():
        new_list_url = id_generator()
        list_urls = db.session.query(List).with_entities(List.url)
        # If random listid (url) is already in the table, we should roll again
        while new_list_url in list_urls:
            new_list_url = id_generator()
        new_list_name = f'My to-do list {dt.now().strftime("%d.%m.%y")}'
        new_list = List(url=new_list_url, name=new_list_name)
        db.session.add(new_list)
        db.session.commit()
        # Retrieving list id #
        new_list_id = db.session.query(List).with_entities(List.listid).filter(List.url == new_list_url)
        first_task = Task(listid=new_list_id, description=new_list_form.description.data, done=0)
        db.session.add(first_task)
        db.session.commit()
        return redirect(url_for('show_list', list_url=new_list_url, new_list_created=True))
    return render_template('index.html', search_form=search_form, new_list_form=new_list_form,
                           new_list_created=new_list_created, new_list_id=new_list_url)

@app.route('/')
def redirect_to_home():
    return redirect(url_for('new_list'))

@app.route('/<list_url>', methods=["POST", "GET"])
def show_list(list_url, new_list_created=False):
    search_form = SearchList()
    add_task_form = AddTask()
    edit_list_name = EditListName()
    cur_list = db.session.query(Task).join(List, Task.listid == List.listid)\
        .add_columns(Task.taskid)\
        .filter(List.url == list_url).first()
    if search_form.validate_on_submit():
        return redirect(url_for('show_list', list_url=search_form.list_id.data))
    # If such list does not exist
    if cur_list is None:
        return redirect(url_for('new_list'))
    cur_list = db.session.query(Task).join(List, Task.listid == List.listid)\
        .add_columns(Task.taskid, Task.description, Task.done, List.name, List.listid, List.url)\
        .filter(List.url == list_url)\
        .order_by(Task.taskid.desc())
    db.session.commit()
    # these entries will be shown in edit_task form in html
    tasks_entries = [task.description for task in cur_list]
    edit_task = EditTask(description=tasks_entries)
    if edit_task.submit5.data and edit_task.validate():
        new_descriptions = edit_task.description.data
        tasks_ids = [task.taskid for task in cur_list]
        for i in range(len(new_descriptions)):
            task_to_update = db.session.query(Task).filter_by(taskid=tasks_ids[i]).first()
            task_to_update.description = new_descriptions[i]
            db.session.commit()
        return render_template('list.html', list=cur_list, list_url=cur_list[0].url, search_form=search_form,
                               add_task_form=add_task_form, new_list_created=new_list_created,
                               edit_list_name=edit_list_name, edit_task=edit_task)

    if edit_list_name.validate_on_submit():
        new_name = edit_list_name.name.data
        list_to_update = db.session.query(List).filter_by(name=cur_list[0].name).first()
        list_to_update.name = new_name
        db.session.commit()
        return redirect(url_for('show_list', list_url=cur_list[0].url))

    if add_task_form.validate_on_submit():
        new_task = Task(description=add_task_form.description.data,
                        done=0, listid=cur_list[0].listid)
        db.session.add(new_task)
        db.session.commit()
        # Erasing task_form
        add_task_form.description.data = ''
        return redirect(url_for('show_list', list_url=cur_list[0].url))

    # If it is a new list
    if request.args.get('new_list_created') == 'True':
        return render_template('list.html', list=cur_list, list_url=cur_list[0].url, search_form=search_form,
                               add_task_form=add_task_form, new_list_created=True,
                               edit_list_name=edit_list_name, edit_task=edit_task)

    return render_template('list.html', list=cur_list, list_url=cur_list[0].url, search_form=search_form,
                           add_task_form=add_task_form, new_list_created=new_list_created,
                               edit_list_name=edit_list_name, edit_task=edit_task)

@app.route("/delete")
def delete():
    id = request.args.get('id')
    list_url = request.args.get('list_url')
    task_to_delete = Task.query.get(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    list_to_check = db.session.query(Task).join(List, Task.listid == List.listid)\
        .add_columns(Task.taskid)\
        .filter(List.url == list_url).first()
    # Check if list is empty
    if list_to_check is not None:
        return redirect(url_for('show_list', list_url=list_url))
    else:
        # Delete list
        list_to_delete = db.session.query(List).filter(List.url == list_url).first()
        db.session.delete(list_to_delete)
        db.session.commit()
        return redirect(url_for('new_list'))

if __name__ == '__main__':
    app.run(threaded=True, port=5000, debug=False)
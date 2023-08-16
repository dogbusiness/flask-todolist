import datetime
from uuid import uuid4

import interface.forms as forms
from core.database import db
from core.models import List, Task
from flask import Blueprint, redirect, render_template, request, url_for

bp = Blueprint(
    "tasks", __name__, static_folder="static", template_folder="templates"
)  # noqa: E501


@bp.route("/search")
def search_list():
    search_form = forms.SearchList()
    if search_form.validate_on_submit():
        return redirect(
            url_for("tasks.show_list", list_url=search_form.list_id.data)
        )  # noqa: E501


@bp.route("/new", methods=["POST", "GET"])
def new_list():
    search_form = forms.SearchList()
    new_list_form = forms.CreateNewList()
    new_list_created = False
    new_list_url = None
    if search_form.validate_on_submit():
        return redirect(
            url_for("tasks.show_list", list_url=search_form.list_id.data)
        )  # noqa: E501
    if new_list_form.validate_on_submit():
        new_list_url = str(uuid4())
        list_urls = db.session.query(List).with_entities(List.url)
        # If random listid (url) is already in the table, we should roll again
        while new_list_url in list_urls:
            new_list_url = str(uuid4())
        new_list_name = f'My to-do list {datetime.datetime.now().strftime("%d.%m.%y")}'  # noqa: E501
        new_list = List(url=new_list_url, name=new_list_name)
        db.session.add(new_list)
        db.session.commit()
        # Retrieving list id #
        new_list_id = (
            db.session.query(List)
            .with_entities(List.listid)
            .filter(List.url == new_list_url)
        )
        first_task = Task(
            listid=new_list_id,
            description=new_list_form.description.data,
            done=0,  # noqa: E501
        )
        db.session.add(first_task)
        db.session.commit()
        return redirect(
            url_for(
                "tasks.show_list", list_url=new_list_url, new_list_created=True
            )  # noqa: E501
        )
    return render_template(
        "index.html",
        search_form=search_form,
        new_list_form=new_list_form,
        new_list_created=new_list_created,
        new_list_id=new_list_url,
    )


@bp.route("/")
def redirect_to_home():
    return redirect(url_for("tasks.new_list"))


@bp.route("/<list_url>", methods=["POST", "GET"])
def show_list(list_url, new_list_created=False):
    search_form = forms.SearchList()
    add_task_form = forms.AddTask()
    edit_list_name = forms.EditListName()
    cur_list = (
        db.session.query(Task)
        .join(List, Task.listid == List.listid)
        .add_columns(Task.taskid)
        .filter(List.url == list_url)
        .first()
    )
    if search_form.validate_on_submit():
        return redirect(
            url_for("tasks.show_list", list_url=search_form.list_id.data)
        )  # noqa: E501
    # If such list does not exist
    if cur_list is None:
        return redirect(url_for("tasks.new_list"))
    cur_list = (
        db.session.query(Task)
        .join(List, Task.listid == List.listid)
        .add_columns(
            Task.taskid,
            Task.description,
            Task.done,
            List.name,
            List.listid,
            List.url,  # noqa: E501
        )
        .filter(List.url == list_url)
        .order_by(Task.taskid.desc())
    )
    db.session.commit()
    # these entries will be shown in edit_task form in html
    tasks_entries = [task.description for task in cur_list]
    edit_task = forms.EditTask(description=tasks_entries)
    if edit_task.submit5.data and edit_task.validate():
        new_descriptions = edit_task.description.data
        tasks_ids = [task.taskid for task in cur_list]
        for i in range(len(new_descriptions)):
            task_to_update = (
                db.session.query(Task).filter_by(taskid=tasks_ids[i]).first()
            )
            task_to_update.description = new_descriptions[i]
            db.session.commit()
        return render_template(
            "list.html",
            list=cur_list,
            list_url=cur_list[0].url,
            search_form=search_form,
            add_task_form=add_task_form,
            new_list_created=new_list_created,
            edit_list_name=edit_list_name,
            edit_task=edit_task,
        )

    if edit_list_name.validate_on_submit():
        new_name = edit_list_name.name.data
        list_to_update = (
            db.session.query(List).filter_by(name=cur_list[0].name).first()
        )  # noqa: E501
        list_to_update.name = new_name
        db.session.commit()
        return redirect(url_for("tasks.show_list", list_url=cur_list[0].url))

    if add_task_form.validate_on_submit():
        new_task = Task(
            taskid=str(uuid4()),
            description=add_task_form.description.data,
            done=0,
            listid=cur_list[0].listid,
        )
        db.session.add(new_task)
        db.session.commit()
        # Erasing task_form
        add_task_form.description.data = ""
        return redirect(url_for("tasks.show_list", list_url=cur_list[0].url))

    # If it is a new list
    if request.args.get("new_list_created") == "True":
        return render_template(
            "list.html",
            list=cur_list,
            list_url=cur_list[0].url,
            search_form=search_form,
            add_task_form=add_task_form,
            new_list_created=True,
            edit_list_name=edit_list_name,
            edit_task=edit_task,
        )

    return render_template(
        "list.html",
        list=cur_list,
        list_url=cur_list[0].url,
        search_form=search_form,
        add_task_form=add_task_form,
        new_list_created=new_list_created,
        edit_list_name=edit_list_name,
        edit_task=edit_task,
    )


@bp.route("/delete")
def delete():
    id = request.args.get("id")
    list_url = request.args.get("list_url")
    task_to_delete = Task.query.get(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    list_to_check = (
        db.session.query(Task)
        .join(List, Task.listid == List.listid)
        .add_columns(Task.taskid)
        .filter(List.url == list_url)
        .first()
    )
    # Check if list is empty
    if list_to_check is not None:
        return redirect(url_for("tasks.show_list", list_url=list_url))
    else:
        # Delete list
        list_to_delete = (
            db.session.query(List).filter(List.url == list_url).first()
        )  # noqa: E501
        db.session.delete(list_to_delete)
        db.session.commit()
        return redirect(url_for("tasks.new_list"))

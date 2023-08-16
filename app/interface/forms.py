from flask_wtf import FlaskForm
from wtforms import FieldList, StringField, SubmitField
from wtforms.validators import DataRequired


class SearchList(FlaskForm):
    list_id = StringField(
        "ListID",
        validators=[DataRequired()],
        render_kw={"placeholder": "Search List by ID"},
    )
    submit1 = SubmitField("Search")


class CreateNewList(FlaskForm):
    description = StringField(
        "Write your task here.",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "Enter your first task and press enter to save."
        },  # noqa: E501
    )
    submit2 = SubmitField("Submit")


class AddTask(FlaskForm):
    description = StringField(
        "Write your task here.",
        validators=[DataRequired()],
        render_kw={"placeholder": "Write your task here."},
    )
    submit3 = SubmitField("Submit")


class EditListName(FlaskForm):
    name = StringField("List Name", validators=[DataRequired()])
    submit4 = SubmitField("Submit")


edit_task_field = StringField("Edit Task", validators=[DataRequired()])


class EditTask(FlaskForm):
    description = FieldList(edit_task_field)
    submit5 = SubmitField("Submit")

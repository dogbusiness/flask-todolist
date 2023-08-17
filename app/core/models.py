from uuid import uuid4

from .database import db


class Task(db.Model):
    __tablename__ = "task"
    taskid = db.Column(db.Integer, primary_key=True)
    listid = db.Column(
        db.Integer, db.ForeignKey("list.listid"), nullable=False
    )  # noqa: E501
    description = db.Column(db.String(300))
    done = db.Column(db.Integer, nullable=False)


class List(db.Model):
    __tablename__ = "list"
    listid = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(36), default=str(uuid4()), unique=True)
    name = db.Column(db.String(200))
    listids = db.relationship("Task", backref="task")

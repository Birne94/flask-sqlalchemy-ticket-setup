import enum

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy.ext.declarative import declared_attr


db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = db.Column(db.Integer, primary_key=True)


class TimestampMixin(object):
    created_on = db.Column(db.DateTime, server_default=func.now())
    updated_on = db.Column(db.DateTime, server_default=func.now(),
                           onupdate=func.now())


class TicketStatus(enum.Enum):
    open = 'open'
    in_progess = 'in_progress'
    rejected = 'rejected'
    closed = 'closed'

    all = (open, in_progess, rejected, closed)


class Ticket(AbstractConcreteBase, TimestampMixin, Base):
    status = db.Column(db.Enum(TicketStatus), nullable=False,
                       default=TicketStatus.open)

    @declared_attr
    def __mapper_args__(cls):
        if cls == Ticket:
            return {'concrete': False}
        return {
            'polymorphic_identity': cls.__name__,
            'concrete': True
        }


class TestTicket(Ticket):
    data = db.Column(db.String, nullable=False)

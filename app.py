from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from models import db, TestTicket, TicketStatus, Ticket

app = Flask(__name__)

db.init_app(app)

with app.app_context():
    db.create_all()
    db.session.commit()


@app.route('/')
def index():
    # This will fail on the first run
    try:
        result = db.session.query(Ticket) \
            .filter(Ticket.status == TicketStatus.open) \
            .all()
    except:
        print('query failed')
    else:
        print('query successful')

    # If I query the subclass, everything will work fine
    db.session.query(TestTicket) \
        .filter(Ticket.status == TicketStatus.open) \
        .all()

    # Try running the query again
    try:
        result = db.session.query(Ticket) \
            .filter(Ticket.status == TicketStatus.open) \
            .all()
    except:
        print('query failed on second try')
    else:
        print('query successful on second try')

    return '', 200


if __name__ == '__main__':
    app.run(debug=True)

from . import db


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    subscribe = db.Column(db.Integer, nullable=False)
    deal = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return 'Sale of ' % self.date.strftime('%Y-%m-%d')

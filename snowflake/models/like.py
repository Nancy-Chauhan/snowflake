from datetime import datetime

from ..db import db


class Like(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)

    created_at = db.Column(db.DateTime, lambda _: datetime.now())

    created_by_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    created_by = db.relationship('User', backref=db.backref('likes', lazy=True))

    appreciation_id = db.Column(db.String, db.ForeignKey('appreciation.id'), nullable=False)
    appreciation = db.relationship('Appreciation')

    @property
    def user_id(self):
        return self.created_by_id

    @property
    def user(self):
        return self.created_by

    @staticmethod
    def create(like):
        db.session.add(like)
        db.session.commit()

    @staticmethod
    def get_by_appreciation(appreciation):
        return Like.query.filter_by(appreciation_id=appreciation.id).all()

    @staticmethod
    def dislike(appreciation, user):
        like = Like.query.filter_by(appreciation_id=appreciation.id, user_id=user.id).first()
        db.session.delete(like)
        db.session.commit()

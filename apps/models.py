# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.policy import default
from apps import db
from sqlalchemy.exc import SQLAlchemyError
from apps.exceptions.exception import InvalidUsage
import datetime as dt
from sqlalchemy.orm import relationship
from enum import Enum

class CURRENCY_TYPE(Enum):
    usd = 'usd'
    eur = 'eur'

class Product(db.Model):

    __tablename__ = 'products'

    id            = db.Column(db.Integer,      primary_key=True)
    name          = db.Column(db.String(128),  nullable=False)
    info          = db.Column(db.Text,         nullable=True)
    price         = db.Column(db.Integer,      nullable=False)
    currency      = db.Column(db.Enum(CURRENCY_TYPE), default=CURRENCY_TYPE.usd, nullable=False)

    date_created  = db.Column(db.DateTime,     default=dt.datetime.utcnow())
    date_modified = db.Column(db.DateTime,     default=db.func.current_timestamp(),
                                               onupdate=db.func.current_timestamp())
    
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    def __repr__(self):
        return f"{self.name} / ${self.price}"

    @classmethod
    def find_by_id(cls, _id: int) -> "Product":
        return cls.query.filter_by(id=_id).first() 

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return


#__MODELS__
class Chess_Piece(db.Model):

    __tablename__ = 'Chess_Piece'

    id = db.Column(db.Integer, primary_key=True)

    #__Chess_Piece_FIELDS__
    rank = db.Column(db.String(255),  nullable=True)
    color = db.Column(db.String(255),  nullable=True)
    status = db.Column(db.String(255),  nullable=True)
    user_id = db.Column(db.Integer, nullable=True)
    soldier_id = db.Column(db.Integer, nullable=True)

    #__Chess_Piece_FIELDS__END

    def __init__(self, **kwargs):
        super(Chess_Piece, self).__init__(**kwargs)


class Game_Match(db.Model):

    __tablename__ = 'Game_Match'

    id = db.Column(db.Integer, primary_key=True)

    #__Game_Match_FIELDS__
    black_user = db.Column(db.Integer, nullable=True)
    white_user = db.Column(db.Integer, nullable=True)
    winner = db.Column(db.Integer, nullable=True)

    #__Game_Match_FIELDS__END

    def __init__(self, **kwargs):
        super(Game_Match, self).__init__(**kwargs)


class Game_Occupied_Soldiers(db.Model):

    __tablename__ = 'Game_Occupied_Soldiers'

    id = db.Column(db.Integer, primary_key=True)

    #__Game_Occupied_Soldiers_FIELDS__
    game_id = db.Column(db.Integer, nullable=True)
    soldier_id = db.Column(db.Integer, nullable=True)

    #__Game_Occupied_Soldiers_FIELDS__END

    def __init__(self, **kwargs):
        super(Game_Occupied_Soldiers, self).__init__(**kwargs)



#__MODELS__END

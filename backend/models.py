import datetime as _dt
from turtle import back
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import database as _database

class User(_database.Base):
    __tablename__ = "users"
    #id = _sql.Column(_sql.Integer, primary_key=True, autoincrement=True)
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    hashed_password = _sql.Column(_sql.String)

    leads = _orm.relationship("Lead", back_populates="owner")
    #username = _sql.Column(_sql.String(64), nullable=False, unique=True)
    #password = _sql.Column(_sql.String(128), nullable=False)
    
    #created_at = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    #updated_at = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow, onupdate=_dt.datetime.utcnow)

    '''
    def __init__(self, username, password, email):
        self.username = username
        self.password = _hash.pbkdf2_sha256.hash(password)
        self.email = email

    def __repr__(self):
        return "<User(id='%s', username='%s', email='%s')>" % (self.id, self.username, self.email)
    '''
    def verify_password(self, password):
        #return _hash.pbkdf2_sha256.verify(password, self.password)
        return _hash.bcrypt.verify(password, self.hashed_password)
        
    '''
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    '''

class Lead(_database.Base):
    __tablename__ = "leads"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))
    first_name = _sql.Column(_sql.String, index=True)
    last_name = _sql.Column(_sql.String, index=True)
    email = _sql.Column(_sql.String, index=True)
    company = _sql.Column(_sql.String, index=True, default="")
    note = _sql.Column(_sql.String, default="")
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    date_last_updated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow, onupdate=_dt.datetime.utcnow)

    owner = _orm.relationship("User", back_populates="leads")
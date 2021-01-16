# from app import db
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
# from flask_sqlalchemy import SQLAlchemy
from app import db
from flask import current_app
from sqlalchemy import *
from sqlalchemy.dialects import *
from app.search import add_to_index, remove_from_index, query_index

class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

##### OLD MODELS
db.Model.metadata.reflect(db.engine)
AutoMapModel = automap_base(db.Model)

class User_Reviews(AutoMapModel):
    __table__ = db.Model.metadata.tables['user_reviews']

    def __repr__(self):
        return '<User_Reviews %r>' % self.id
# AutoMapModel.prepare(db.engine, reflect = True)

class Users(AutoMapModel):
    __table__ = db.Model.metadata.tables['users']

    def __repr__(self):
        return '<Users %r>' % self.username
AutoMapModel.prepare(db.engine, reflect = True)

class Products(AutoMapModel):
    __searchable__ = ['body']
    __table__ = db.Model.metadata.tables['products']

    def __repr__(self):
        return '<Products %r>' % self.product_name
AutoMapModel.prepare(db.engine, reflect = True)


##### MAIN MODELS
# class User_Reviews(db.Model):
#     __searchable__ = ['body']
#     # __table__ = db.Model.metadata.tables['user_reviews']
#     __tablename__ = 'user_reviews'
#     __table_args__ = {'extend_existing': True}
#     from app import db
#     id= db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.Text)
#     skin_tone = db.Column(db.Text)
#     skin_type = db.Column(db.Text)
#     product_name = db.Column(db.Text, db.ForeignKey('products.product_name'))
#     rating = db.Column(db.Text)
#     text = db.Column(db.Text)

    
#     def __repr__(self):
#         return '<User_Reviews %r>' % self.id
# # AutoMapModel.prepare(db.engine, reflect = True)

# class Users(db.Model):
#     # __table__ = db.Model.metadata.tables['users']
#     __tablename__ = 'users'
#     __table_args__ = {'extend_existing': True}
    
#     id = db.Column(db.Integer, primary_key =True)
#     username = db.Column(db.String)
#     skin_tone = db.Column(db.String)
#     skin_type = db.Column(db.String)

#     def __repr__(self):
#         return '<Users %r>' % self.username
# # AutoMapModel.prepare(db.engine, reflect = True)

# class Products(SearchableMixin, db.Model):
#     __searchable__ = ['body']
#     # __table__ = db.Model.metadata.tables['products']
#     __tablename__ = 'products'
#     __table_args__ = {'extend_existing': True}
#     product_name = db.Column(db.String, primary_key=True)
#     brand = db.Column(db.String, nullable=True)
#     categories = db.Column(db.Text, nullable = True)
#     no_of_review = db.Column(db.Integer)
#     price = db.Column(db.Float)
#     overall_rating = db.Column(db.Integer)
#     keywords = db.Column(db.Text)
#     user_review_recommendations = db.Column(db.Text)
#     rating_recommendations = db.Column(db.Text)

#     def __repr__(self):
#         return '<Products %r>' % self.product_name
# # AutoMapModel.prepare(db.engine, reflect = True)
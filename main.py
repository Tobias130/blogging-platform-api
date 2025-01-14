from datetime import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_restful import Resource, Api, fields, marshal_with, abort, reqparse


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)
api = Api(app)

class PostModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    tags = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Post(title= {self.title}, content = {self.content}, category = {self.content}, tags = {self.tags})"

post_args = reqparse.RequestParser()
post_args.add_argument('title', type=str, required=True, help="Title cannot be blank")
post_args.add_argument('content', type=str, required=True, help="Content cannot be blank")
post_args.add_argument('category', type=str, required=True, help="Category cannot be blank")
post_args.add_argument('tags', type=list, required=True, help="Tags cannot be blank", location='json')

post_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'category': fields.String,
    'tags': fields.Raw,
    'created_at': fields.DateTime(dt_format='iso8601'),
    'updated_at': fields.DateTime(dt_format='iso8601')
}

class Posts(Resource):
    @marshal_with(post_fields)
    def get(self):
        search_term = request.args.get('term', '')

        if(search_term):
            search = f"%{search_term}%"
            posts = PostModel.query.filter(
                or_(
                    PostModel.title.ilike(search),
                    PostModel.content.ilike(search),
                    PostModel.category.ilike(search)
                )
            ).all()
        else:
            posts = PostModel.query.all()
        return posts

    @marshal_with(post_fields)
    def post(self):
        args = post_args.parse_args()
        post = PostModel(title=args['title'], content=args['content'], category=args['category'], tags=args['tags'])
        db.session.add(post)
        db.session.commit()
        posts = PostModel.query.all()
        return posts, 201

class Post(Resource):
    @marshal_with(post_fields)
    def get(self, id):
        post = PostModel.query.filter_by(id=id).first()
        if not post:
            abort(404, message="Post not found")
        return post

    @marshal_with(post_fields)
    def put(self, id):
        args = post_args.parse_args()
        post = PostModel.query.filter_by(id=id).first()
        if not post:
            abort(404, message="Post not found")
        post.title = args['title']
        post.content = args['content']
        post.category = args['category']
        post.tags = args['tags']
        db.session.commit()
        return post

    @marshal_with(post_fields)
    def delete(self, id):
        post = PostModel.query.filter_by(id=id).first()
        if not post:
            abort(404, message="Post not found")
        db.session.delete(post)
        db.session.commit()
        posts = PostModel.query.all()
        return posts

api.add_resource(Posts, '/posts/')
api.add_resource(Post, '/posts/<int:id>')

@app.route('/')
def home():
    return '<h1>API</h1>'

if __name__ == "__main__":
    app.run(debug=True)

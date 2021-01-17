from flask import Flask, request, session, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from spam import replace_username
import os
app = Flask(__name__)

CORS(app, supports_credentials=True)

app.secret_key = os.environ.get('SECRET_KET')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Database initialization
db = SQLAlchemy(app)


class Comment(db.Model):
    id = db.Column(db.Integer, db.Sequence('comment_id_seq'), primary_key=True)
    path = db.Column(db.String(), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    post_slug = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(), nullable=False)
    published_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def __init__(self, id, path, level, post_slug, username, message, published_time):
        self.id = id
        self.path = path
        self.level = level
        self.post_slug = post_slug
        self.username = username
        self.message = message
        self.published_time = published_time
    def to_dict(self):
        return {
            'path':self.path,
            'level':self.level,
            'username': self.username,
            'message': self.message,
            'published_time': self.published_time
        }

@app.route("/")
def homepage():
    return "<h1>Hello, This is my simple comment system for Classic of Data blog.</h1>"

@app.route('/api/user/logout', methods=['POST'])
def logout():
    if request.method == 'POST':
        session.pop('username')
    return jsonify({'username': session.get('username')})

@app.route('/api/user/status', methods=['GET'])
def login_status():
    if request.method == 'GET':
        return jsonify({'status': session.get('username', False)})


@app.route("/api/comment/new", methods=["POST"])
def create_comment():
    if request.method == "POST":
        try:
            data = request.get_json()
            id = db.session.execute(db.Sequence('comment_id_seq'))
            level = data['path'].count('p')+1
            path = data['path']+f'p{id}'
            post_slug = data['post_slug']
            if 'username' in data:
                session['username'] = replace_username(data['username'])
            username = replace_username(data.get('username','anonymous'))
            message = data['message']
            published_time = db.func.current_timestamp()
            comment = Comment(id, path, level, post_slug,
                                username, message, published_time)

            db.session.add(comment)
            db.session.commit()
            return {'status': True}
        except Exception as e:
            print(e)
            return {'status': False}

@app.route("/api/comment/<slug>",methods=["GET"])
def get_comment(slug):
    if request.method == "GET":
        comments = Comment.query.filter_by(post_slug = slug).order_by(Comment.path).all()
        return jsonify([comment.to_dict() for comment in comments])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, jsonify, render_template, request, abort
from functools import wraps
from os import environ as env
from datetime import datetime
import dataset

db = dataset.connect(env['DATABASE_URL'])

app = Flask(__name__)

def require_permission(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('password') == env['PWD']:
            return jsonify({'error':'You are not authorized!'})

        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def home():
    posts = db['posts'].find(order_by='-created_at')

    return render_template('home.html', posts=posts)

@app.route("/<slug>")
def show_post(slug):
    post = db['posts'].find_one(slug=slug)
    post['body'] = '<br>'.join(post['body'].split('\n'))

    return render_template('posts/show.html', post=post)

@app.route("/<slug>", methods=["POST"])
@require_permission
def upsert_post(slug):
    title = request.headers.get('title', slug)
    body = request.data

    post = dict(slug=slug, title=title, body=body, created_at=datetime.now())

    db['posts'].upsert(post, ['slug'])

    return jsonify(post)

@app.route("/<slug>", methods=["DELETE"])
@require_permission
def delete_post(slug):
    post = dict(db['posts'].find_one(slug=slug))
    db['posts'].delete(slug=slug)
    return jsonify(post)


if __name__=="__main__":
    app.run(debug=True)

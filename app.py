from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@app.route('/')
def home():
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/add_post', methods=['POST'])
def add_post():
    title = request.form['title']
    content = request.form['content']
    new_post = BlogPost(title=title, content=content)
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

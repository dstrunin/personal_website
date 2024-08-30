import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'blog.db')
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Add this line
print(f"Database should be created at: {os.path.join(basedir, 'blog.db')}")  # Add this line

db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@app.route('/')
def home():
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
    print(f"Number of posts: {len(posts)}")  # Add this line
    for post in posts:
        print(f"Post: {post.title}")  # Add this line
    return render_template('index.html', posts=posts)

@app.route('/admin')
def admin():
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
    return render_template('admin.html', posts=posts)

@app.route('/add_post', methods=['POST'])
def add_post():
    title = request.form['title']
    content = request.form['content']
    new_post = BlogPost(title=title, content=content)
    db.session.add(new_post)
    db.session.commit()
    print(f"New post added: {title}")  # Add this line
    return redirect(url_for('home'))

@app.route('/check_posts')
def check_posts():
    posts = BlogPost.query.all()
    return '<br>'.join([f"{post.id}: {post.title}" for post in posts])

@app.route('/delete_post/<int:id>', methods=['POST'])
def delete_post(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Post has been deleted!', 'success')
    return redirect(url_for('admin'))

@app.route('/edit_post/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.date_posted = datetime.now()
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('admin'))
    return render_template('edit_post.html', post=post)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created")  # Add this line
    app.run(debug=True)

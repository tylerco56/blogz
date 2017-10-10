from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model): 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    entry = db.Column(db.String(500))
    #owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, entry):
        self.title = title
        self.entry = entry
        #self.owner = owner

@app.route('/', methods=['POST', 'GET'])
def index():

    #owner = User.query.filter_by(email=session['email']).first()

    if request.method == 'POST':
        title = request.form['title']
        entry = request.form['entry']
        new_entry = Blog(title, entry)
        db.session.add(new_entry)
        db.session.commit()

    blogs = Blog.query.all()


    #tasks = Task.query.filter_by(completed=False,owner=owner).all()
    #completed_tasks = Task.query.filter_by(completed=True,owner=owner).all()
    return render_template('blog.html', website_title="Super Awesome Blog", blogs=blogs)

if __name__ == '__main__':
    app.run()
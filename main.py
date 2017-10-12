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

@app.route('/')
def redirect_to_blog():
        return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def index():
    #owner = User.query.filter_by(email=session['email']).first()
    title = ""
    entry = ""
    title_error = ""
    entry_error = ""
    entry_id = ""
    newpost_id = ""
    
    if request.method == 'POST':
        title = request.form['title']
        entry = request.form['entry']
        
        if title == "":
            title_error = "Please enter a title!"
        if entry == "":
            entry_error = "Please enter a body!"
            
        if title and entry:
            new_entry = Blog(title, entry)
            db.session.add(new_entry)
            db.session.commit()
            newpost_id = new_entry.id
        else:
            return render_template('newpost.html', title=title, entry=entry, title_error=title_error, entry_error=entry_error)
    
    entry_id = request.args.get('id')
    
    if entry_id:
        blogs = Blog.query.filter_by(id=entry_id)
    elif newpost_id:
        blogs = Blog.query.filter_by(id=newpost_id)
    else:
        blogs = Blog.query.all()

    #tasks = Task.query.filter_by(completed=False,owner=owner).all()
    #completed_tasks = Task.query.filter_by(completed=True,owner=owner).all()
    return render_template('blog.html', website_title="Super Awesome Blog", blogs=blogs)

@app.route('/blog_entry', methods=['POST', 'GET'])
def create_entry():



    return render_template('blog-entry.html', title=title, entry=entry)

@app.route('/newpost')
def write_a_entry():
    return render_template('newpost.html')



if __name__ == '__main__':
    app.run()
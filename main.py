from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "doodle"

class Blog(db.Model): 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    entry = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")

    def __init__(self, title, entry, owner):
        self.title = title
        self.entry = entry
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120)) 
    password = db.Column(db.String(120))
    blogs = db.relationship("Blog", backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request  #run this function before you run any incoming request handler
def require_login():
    allowed_routes = ['login', 'signup', 'blog', 'index'] #setting the variable of allowed routes to /login and /register 
    print(session)                                 #so you don't have to be logged in to view these pages 
       #request.endpoint path from form ex: login or register
    if request.endpoint not in allowed_routes and 'user' not in session: 
        return redirect('/login')

@app.route('/add', methods=['POST', 'GET'])
def add():
    #if title == "":
        #title_error = "Please enter a title!"
    #if entry == "":
        #entry_error = "Please enter a body!"
    if request.method == 'POST':
        title = request.form['title']
        entry = request.form['entry']
        owner = User.query.filter_by(username=session['user']).first()

        #if title and entry:
        new_entry = Blog(title, entry, owner)
        db.session.add(new_entry)
        db.session.commit()
        newpost_id = new_entry.id
        content = Blog.query.get(newpost_id)

        return render_template("blog.html", display_one=content)

    return render_template("newpost.html")


@app.route('/blog', methods=['POST', 'GET'])
def blog():
    
    entry_id = request.args.get('id')
    owner_id = request.args.get('oid') 


    if entry_id:
        content = Blog.query.filter_by(id=entry_id)
    elif owner_id:
        content = Blog.query.filter_by(owner_id=owner_id)
    else:
        content = Blog.query.all()
    
    return render_template("blog.html", content=content)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username'] #uses name="email" from register from
        password = request.form['password'] #uses name="password" from register.html
        verify = request.form['verify'] #uses name="verify" from register.html form
        existing_user = User.query.filter_by(username=username).first()

        username_error = ""
        username_error_flag = False
        password_error = ""
        verify_password_error = ""
        erase_passwords = False
        email_error = ""
        error_flag = False

        if not username:
            flash("Please Enter an User Name.")
            error_flag = True

        if not password:
            flash("Please Enter a Password.")
            erase_passwords = True
            error_flag = True

        if not verify:
            flash("Please Enter Another Password to Verify.")
            erase_passwords = True
            error_flag = True

        if existing_user:
            flash("The username exists. Please enter another name.")
            error_flag = True

        if not password == verify:
            flash("Your passwords do not match.")
            erase_passwords = True
            error_flag = True

        if len(username) < 3:
            flash("Username must be at least 3 characters")
            erase_passwords = True
            error_flag = True
        
        if len(verify) < 3 or len(password) < 3:
            flash("Password must be at least 3 characters")
            erase_passwords = True
            error_flag = True

        if erase_passwords:
            password = ""
            verify = ""

        if not existing_user and not error_flag:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['user'] = username #creates a dictionary that keeps track of session with email
            return redirect('/add')


    return render_template('signup.html')



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['user']  #gets data from a POST form in login.html with name="email" from input box
        password = request.form['password'] #gets data from a POST form in login.html with name="password" from input box
        user_check = User.query.filter_by(username=user).first() #retrieves the one item from a query
                                            #if it retrieves nothing it will equal ***None*** *without quots
        if user_check and user_check.password == password:
            session['user'] = user  #creates a dictionary that keeps track of session with email
            flash("Logged in") #flash uses the with statement on the base.html
            return redirect('/add')
        
        if user_check == None:
            flash('User does not exist', 'error') #flash uses the with statement on the base.html
            password = "" 

        if user_check and user_check.password != password:
            flash('Password is incorrect', 'error')
            password = ""

    return render_template('login.html')    
    
@app.route('/')
def index():
    users = User.query.all()

    return render_template('index.html', users = users)
    

@app.route('/logout')
def logout():
    del session['user']
    return redirect('/blog')


@app.route('/blog_entry', methods=['POST', 'GET'])
def create_entry():
    return render_template('blog-entry.html', title=title, entry=entry)



if __name__ == '__main__':
    app.run()
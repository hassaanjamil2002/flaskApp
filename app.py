from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Make sure this folder exists
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit upload size to 16 MB
# Set up the database connection    
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Create the User model (table)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    profile_picture = db.Column(db.String(200))
    bio = db.Column(db.Text)
    skills = db.Column(db.String(200))
    online_profiles = db.Column(db.String(200))

    def __init__(self, first_name, last_name, email, phone, profile_picture, bio, skills, online_profiles):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.profile_picture = profile_picture
        self.bio = bio
        self.skills = skills
        self.online_profiles = online_profiles

# Initialize the database tables (run this once)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create-portfolio', methods=['GET', 'POST'])
def create_portfolio():
    if request.method == 'POST':
        try:
            # Get the form data
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            phone = request.form['phone']
            bio = request.form['bio']
            skills = request.form['skills']
            online_profiles = request.form['online_profiles']
            
            # Save the profile picture if uploaded
            profile_picture_path = request.form['profile_picture']
                

            # Create a new User instance
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                profile_picture=profile_picture_path,
                bio=bio,
                skills=skills,
                online_profiles=online_profiles
            )
            
            # Add to the database
            db.session.add(new_user)
            db.session.commit()

            return "<h1>Account created and saved successfully!</h1>"

        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return "<h1>There was an error saving the account. Check the logs for details.</h1>"
    
    return render_template('create_account.html')

@app.route('/view-portfolio', methods=['GET', 'POST'])
def view_portfolio():
    if request.method == 'POST':
        # Get the search email from the form
        search_email = request.form['search_email']
        # Query the user by email
        users = User.query.filter_by(email=search_email).all()
        return render_template('view_portfolio.html', users=users)

    # If GET request, fetch all users
    users = User.query.all()
    return render_template('view_portfolio.html', users=users)

@app.route('/about')
def about():
    return render_template('about_me.html')
from flask import send_from_directory

# Route to serve profile pictures (if they are in a specific folder like "uploads")
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)

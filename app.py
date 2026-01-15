from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from config import Config
from dotenv import load_dotenv
import os

# Load .env only locally
if os.getenv("RENDER") is None:
    load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
mail = Mail(app)

# ================== CREATE TABLES (IMPORTANT) ==================
# This ensures tables are created automatically on Render
with app.app_context():
    db.create_all()

# ================== MODELS ==================
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tech_stack = db.Column(db.String(200))
    image_url = db.Column(db.String(200), default='default_project.jpg')
    live_link = db.Column(db.String(200))
    github_link = db.Column(db.String(200))

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    institution = db.Column(db.String(200), nullable=False)
    degree = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.String(50))
    description = db.Column(db.Text)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer)
    category = db.Column(db.String(50))
    icon = db.Column(db.String(50))

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    tagline = db.Column(db.String(200))
    about_text = db.Column(db.Text)
    email = db.Column(db.String(100))
    linkedin = db.Column(db.String(200))
    github = db.Column(db.String(200))

# ================== ROUTES ==================
@app.route('/')
def index():
    user = UserProfile.query.first()

    if not user:
        user = UserProfile(
            name="Setup Required",
            tagline="Database connected successfully",
            about_text="Tables are created. Seed data next."
        )

    projects = Project.query.limit(3).all()
    skills = Skill.query.all()
    experiences = Experience.query.all()
    educations = Education.query.all()

    return render_template(
        'index.html',
        user=user,
        projects=projects,
        skills=skills,
        experiences=experiences,
        educations=educations
    )

@app.route('/projects')
def projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        msg = Message(
            subject=f"Subject: {subject}",
            recipients=['agnihotrigaurav659@gmail.com'],
            body=f"From: {name} <{email}>\n\n{message}"
        )

        try:
            mail.send(msg)
            flash('Message sent successfully!', 'success')
        except Exception as e:
            flash(f'Error sending message: {str(e)}', 'danger')

        return redirect(url_for('contact'))

    return render_template('contact.html')

if __name__ == "__main__":
    app.run()

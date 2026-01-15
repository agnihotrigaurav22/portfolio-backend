from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from config import Config
from dotenv import load_dotenv
import os

# ================== ENV SETUP ==================
# Load .env only locally (Render already has env vars)
if os.getenv("RENDER") is None:
    load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
mail = Mail(app)

# ================== MODELS ==================
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tech_stack = db.Column(db.String(200))
    image_url = db.Column(db.String(200), default="default_project.jpg")
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

# ================== DB INIT + SEED (RUNS ONCE) ==================
with app.app_context():
    db.create_all()

    # Seed ONLY if database is empty
    if UserProfile.query.first() is None:

        # -------- User Profile --------
        user = UserProfile(
            name="Gaurav Agnihotri",
            tagline="Data Science Undergraduate at IIT Madras | AI/ML Enthusiast",
            about_text=(
                "Data Science undergraduate at IIT Madras with hands-on experience in "
                "machine learning, data analysis, and model evaluation. Seeking AI/ML "
                "internship opportunities to build, validate, and deploy data-driven "
                "models for real-world problem solving."
            ),
            email="agnihotrigaurav659@gmail.com",
            linkedin="https://linkedin.com/in/agnihotrigaurav659",
            github="https://github.com/agnihotrigaurav22"
        )
        db.session.add(user)

        # -------- Education --------
        edu = Education(
            institution="Indian Institute of Technology Madras",
            degree="Bachelor of Science (BS) in Data Science and Applications",
            duration="2023 – 2027",
            description=""
        )
        db.session.add(edu)

        # -------- Skills --------
        skills = [
            Skill(name="Python", level=90, category="Language", icon="fab fa-python"),
            Skill(name="SQL", level=85, category="Language", icon="fas fa-database"),
            Skill(name="HTML5", level=90, category="Language", icon="fab fa-html5"),
            Skill(name="CSS", level=85, category="Language", icon="fab fa-css3-alt"),

            Skill(name="Flask", level=85, category="Framework", icon="fas fa-flask"),
            Skill(name="NumPy/Pandas", level=85, category="Data Science", icon="fas fa-table"),
            Skill(name="Scikit-learn", level=80, category="Machine Learning", icon="fas fa-brain"),
            Skill(name="Streamlit", level=80, category="Framework", icon="fas fa-chart-bar"),

            Skill(name="Git/GitHub", level=90, category="Tool", icon="fab fa-github"),
            Skill(name="Docker", level=70, category="DevOps", icon="fab fa-docker"),
        ]
        db.session.add_all(skills)

        # -------- Experience --------
        experiences = [
            Experience(
                role="AI and Cloud Intern",
                company="IBM",
                duration="Sep 2025 – Oct 2025",
                description=(
                    "Analyzed and processed large datasets, performing feature engineering "
                    "and data visualization. Collaborated with cross-functional teams to "
                    "design and implement RESTful APIs for scalable AI-driven applications."
                )
            ),
            Experience(
                role="Teaching Assistant, C Programming Lab",
                company="IIT Madras",
                duration="Jun 2024 – Dec 2024",
                description=(
                    "Assisted undergraduate students in debugging, optimizing, and improving "
                    "C programs. Provided guidance on syntax, logical reasoning, and "
                    "effective problem-solving techniques."
                )
            )
        ]
        db.session.add_all(experiences)

        # -------- Projects --------
        projects = [
            Project(
                title="Cinema Audience Forecasting",
                description="ML regression solution to predict audience count per theatre per show. Built an end-to-end ML pipeline with XGBoost.",
                tech_stack="Python, XGBoost, Pandas, Scikit-learn",
                image_url="https://opengraph.githubassets.com/1/agnihotrigaurav22/Cinema-Audience-Forcasting-ML-Project",
                github_link="https://github.com/agnihotrigaurav22/Cinema-Audience-Forcasting-ML-Project",
                live_link="#"
            ),
            Project(
                title="AI Fitness Planner",
                description="AI-driven web app generating personalized workout and diet plans using Google Gemini API.",
                tech_stack="Flask, Google Gemini API, RESTful APIs",
                image_url="https://opengraph.githubassets.com/1/agnihotrigaurav22/AI-Fitness-Planner",
                github_link="https://github.com/agnihotrigaurav22/AI-Fitness-Planner",
                live_link="#"
            ),
            Project(
                title="Vehicle Parking Management",
                description="Web-based system to automate slot booking and vehicle tracking with SQLite and Bootstrap.",
                tech_stack="Flask, SQLite, Bootstrap, Jinja2",
                image_url="https://opengraph.githubassets.com/1/agnihotrigaurav22/Parkeasy",
                github_link="https://github.com/agnihotrigaurav22/Parkeasy",
                live_link="#"
            )
        ]
        db.session.add_all(projects)

        db.session.commit()
        print("✅ Database seeded successfully.")

# ================== ROUTES ==================
@app.route("/")
def index():
    user = UserProfile.query.first()
    projects = Project.query.limit(3).all()
    skills = Skill.query.all()
    experiences = Experience.query.all()
    educations = Education.query.all()

    return render_template(
        "index.html",
        user=user,
        projects=projects,
        skills=skills,
        experiences=experiences,
        educations=educations
    )

@app.route("/projects")
def projects():
    projects = Project.query.all()
    return render_template("projects.html", projects=projects)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        msg = Message(
            subject=f"Subject: {subject}",
            recipients=["agnihotrigaurav659@gmail.com"],
            body=f"From: {name} <{email}>\n\n{message}"
        )

        try:
            mail.send(msg)
            flash("Message sent successfully!", "success")
        except Exception as e:
            flash(f"Error sending message: {str(e)}", "danger")

        return redirect(url_for("contact"))

    return render_template("contact.html")

if __name__ == "__main__":
    app.run()

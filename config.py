import os

class Config:
    # ================== SECURITY ==================
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

    # ================== DATABASE (MYSQL + SSL) ==================
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.environ['DB_USER']}:"
        f"{os.environ['DB_PASSWORD']}@"
        f"{os.environ['DB_HOST']}:"
        f"{os.environ['DB_PORT']}/"
        f"{os.environ['DB_NAME']}?ssl_disabled=false"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ================== EMAIL ==================
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_USERNAME")

<<<<<<< HEAD
from flask import Flask, session, redirect, url_for, request

app = Flask(__name__)
app.config["SECRET_KEY"] = 'ASDFGHJKL;40XCVBNM'

with open('index.html', "r", encoding="utf-8") as f:
    f =  f.read()

@app.route("/")
def index():
    return f
=======
from flask import Flask, session, redirect, url_for, request, g
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import os

DATABASE = '/tmp/main.db'
DEBUG = True
SECRET_KEY = 'ASDFGHJKL;40XCVBNM'

app = Flask(__name__)
app.config.from_object(__name__)

os.makedirs(app.instance_path, exist_ok=True)
app.config.update(
    DATABASE=os.path.join(app.instance_path, "main.db")
)



def get_db():
    if "db" not in g:
        db_path = app.config.get("DATABASE", os.path.join(app.root_path, "main.db"))
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
        db.commit()


init_db()

with open('index.html', "r", encoding="utf-8") as f:
    index_html =  f.read()
@app.route("/")
def index():
    return index_html
>>>>>>> b3da82f (first commit)
    

@app.route("/login", methods=["POST", "GET"])
def login():
<<<<<<< HEAD
=======
    message = ''
    if request.method == "POST":
        username = request.form.get("email")
        password = request.form.get("password")

        if username and password:
            db = get_db()
            user = db.execute(
                "SELECT id, username, password_hash FROM users WHERE email = ?",
                (username,)
            ).fetchone()

            if user is not None and check_password_hash(user["password_hash"], password):
                session.clear()
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                return redirect(url_for("index"))
        message = "Данный пользователя введены не верно"
        return login_page(message)

>>>>>>> b3da82f (first commit)
    with open("login.html", 'r', encoding='utf-8') as f:
        return f.read()


@app.route("/singin", methods=["POST", "GET"])
def singin():
<<<<<<< HEAD
    with open("logon.html", "r", encoding='utf-8') as f:
        return f.read()

# @app.route("/logon", method=["POST", "GET"])
# def logon():
    

=======
    message = ""

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if not username or not email or not password:
            message = "Заполни все поля"

        else:
            email = email.strip().lower()

            db = get_db()

            user = db.execute(
                "SELECT id FROM users WHERE email = ? OR username = ?",
                (email, username)
            ).fetchone()

            if user is not None:
                message = "Данный пользователь уже зарегистрирован"

            else:
                password_hash = generate_password_hash(password)

                db.execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                    (username, email, password_hash)
                )

                db.commit()

                return redirect(url_for("login"))

    return logon_page(message)


def login_page(message=""):
    with open("login.html", "r", encoding="utf-8") as f:
        html = f.read()

    if message:
        message_html = f"""
        <div style="
            color: #ff8080;
            background: rgba(255, 0, 0, 0.08);
            border: 1px solid rgba(255, 0, 0, 0.25);
            padding: 12px 16px;
            border-radius: 12px;
            margin-bottom: 16px;
            font-size: 15px;
            text-align: center;
        ">
            {message}
        </div>
        """

        if "<form" in html:
            html = html.replace("<form", message_html + "\n<form", 1)
        elif "</body>" in html:
            html = html.replace("</body>", message_html + "\n</body>", 1)
        else:
            html = message_html + html

    return html


def logon_page(message=""):
    with open("logon.html", "r", encoding="utf-8") as f:
        html = f.read()

    if message:
        message_html = f"""
        <div style="
            color: #ff8080;
            background: rgba(255, 0, 0, 0.08);
            border: 1px solid rgba(255, 0, 0, 0.25);
            padding: 12px 16px;
            border-radius: 12px;
            margin-bottom: 16px;
            font-size: 15px;
            text-align: center;
        ">
            {message}
        </div>
        """

        if "<form" in html:
            html = html.replace("<form", message_html + "\n<form", 1)
        elif "</body>" in html:
            html = html.replace("</body>", message_html + "\n</body>", 1)
        else:
            html = message_html + html

    return html
>>>>>>> b3da82f (first commit)
    
if __name__ == "__main__":
    app.run(debug=False)
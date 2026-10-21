import os
from flask import Flask, request
from markupsafe import escape
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST", "localhost")
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER", "root")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD", "")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB", "devops")
mysql = MySQL(app)

@app.route("/health")
def health():
    return "ok"

@app.route("/", methods=["GET", "POST"])
def index():
    cur = mysql.connection.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS messages (id INT AUTO_INCREMENT PRIMARY KEY, message TEXT)")
    if request.method == "POST":
        cur.execute("INSERT INTO messages (message) VALUES (%s)", (request.form["message"],))
        mysql.connection.commit()
    cur.execute("SELECT message FROM messages")
    rows = cur.fetchall()
    cur.close()
    items = "".join(f"<li>{escape(r[0])}</li>" for r in rows)
    return f'<form method="post"><input name="message"><button>Send</button></form><ul>{items}</ul>'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

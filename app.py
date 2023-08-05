import datetime as dt
from support import (
    discarder,
    login_required,
    create_showtask,
    score_calc,
    tab_name,
    maslow_word,
    size_word,
)
from cs50 import SQL
from flask import Flask, flash, redirect, session, render_template, request
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# app config
app = Flask(__name__)

# config session, changing default "true" to false and switching to filesystem
# reference to cs50x problem-set "Finance"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# config sql
db = SQL("sqlite:///database.db")

# catch every answer from the server and modify the headers for never saving in cache.
# reference to cs50x problem-set "Finance"
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# The index-page
@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    usid = session["user_id"]

    # get username
    userdata = db.execute("SELECT id, username FROM users WHERE id = ?", usid)[0]

    # get historical datas from scores-table
    scoring = db.execute("SELECT * FROM scores WHERE user_id = ?", usid)
    score = scoring[0]
    total = (
        score["selfdev"]
        + score["ego"]
        + score["socials"]
        + score["security"]
        + score["physics"]
    )

    # actuall statistics
    mas1 = len(
        db.execute(
            "SELECT maslow FROM tasks WHERE user_id = ? AND closed = 0 AND maslow = ?",
            usid,
            1,
        )
    )
    mas2 = len(
        db.execute(
            "SELECT maslow FROM tasks WHERE user_id = ? AND closed = 0 AND maslow = ?",
            usid,
            2,
        )
    )
    mas3 = len(
        db.execute(
            "SELECT maslow FROM tasks WHERE user_id = ? AND closed = 0 AND maslow = ?",
            usid,
            3,
        )
    )
    mas4 = len(
        db.execute(
            "SELECT maslow FROM tasks WHERE user_id = ? AND closed = 0 AND maslow = ?",
            usid,
            4,
        )
    )
    mas5 = len(
        db.execute(
            "SELECT maslow FROM tasks WHERE user_id = ? AND closed = 0 AND maslow = ?",
            usid,
            5,
        )
    )

    sum = mas1 + mas2 + mas3 + mas4 + mas5

    masl = [sum, mas1, mas2, mas3, mas4, mas5]

    return render_template(
        "index.html",
        username=userdata.get("username"),
        score=score,
        total=total,
        masl=masl,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    # forget user_id
    session.clear()

    # if linking to page
    if request.method == "GET":
        return render_template("login.html")

    # if using form
    if request.method == "POST":
        # username submitted
        if not request.form.get("username"):
            return discarder("Bitte Username eingeben.")
        # password submitted
        if not request.form.get("passwort"):
            return discarder("Bitte Passwort eingeben.")
        # connect db
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # check valid user and password
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("passwort")
        ):
            return discarder("Invalid username or password")

        # save user in session
        session["user_id"] = rows[0]["id"]

        # redirect
        flash("loged in")
        return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    # register user
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        # if not everything is typed in
        if (
            not request.form.get("username")
            or not request.form.get("passwort")
            or not request.form.get("wpass")
        ):
            return discarder("Bitte alle Felder ausfüllen.")

        # if password does not match the second password
        elif request.form.get("passwort") != request.form.get("wpass"):
            return discarder("Passwörter stimmen nicht überein.")

        # if user allready exists
        check = db.execute("SELECT username FROM users")
        for person in check:
            if person["username"] == request.form.get("username"):
                return discarder("Username ist schon vergeben.")

        # defining variables
        username = request.form.get("username")
        passwort = generate_password_hash(
            (request.form.get("passwort")), method="pbkdf2", salt_length=16
        )
        # add user to database
        db.execute(
            "INSERT INTO users(username, hash) VALUES (?, ?)", username, passwort
        )
        # login user
        nrows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = nrows[0]["id"]

        # add user to socres
        db.execute("INSERT INTO scores(user_id) VALUES (?)", session["user_id"])

        # redirect to homepage
        flash("account created")
        return redirect("/")


@app.route("/newtask", methods=["GET", "POST"])
@login_required
def newtask():
    if request.method == "GET":
        return render_template("newtask.html")

    if request.method == "POST":
        # define variables to help
        tname = request.form.get("tname")
        size = request.form.get("size")
        category = request.form.get("cat")
        description = request.form.get("description")

        # some checks
        if (
            not request.form.get("tname")
            or not request.form.get("size")
            or not request.form.get("cat")
            or not request.form.get("description")
        ):
            return discarder("all fields have to be filled")

        # defining needed datas for entry
        if request.form.get("boost") == None:
            boost = 0
        else:
            boost = 1

        tname = request.form.get("tname")
        size = request.form.get("size")
        category = request.form.get("cat")
        description = request.form.get("description")
        uid = session["user_id"]
        cdate = "open"
        sdate = dt.datetime.today()
        # add task to db
        db.execute(
            "INSERT INTO tasks (user_id, tname, description, maslow, size, boost, sdate, cdate) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            uid,
            tname,
            description,
            category,
            size,
            boost,
            sdate.date(),
            cdate,
        )
        # redirect
        flash("task created")
        return redirect("/")


@app.route("/showtask", methods=["GET", "POST"])
@login_required
def showtask():
    # building the page
    if request.method == "GET":
        datas = create_showtask()

        return render_template("showtask.html", datas=datas)

    # for closing a task (value to come is the id of the task)
    if request.method == "POST":
        # definitions
        sclose = request.form.get("kill")
        sboost = request.form.get("boost")

        # clsoing a task (via post:id)
        if not sclose == None:
            db.execute("UPDATE tasks SET closed = 1 WHERE id=?", sclose)

            # cdate updaten
            cdate = dt.datetime.today()
            db.execute("UPDATE tasks SET cdate = ? WHERE id=?", cdate.date(), sclose)

            # scores updaten
            rawsc = db.execute(
                "SELECT maslow, size, boost FROM tasks WHERE id=?", sclose
            )
            score = score_calc(rawsc[0]["maslow"], rawsc[0]["size"], rawsc[0]["boost"])
            tab = tab_name(rawsc[0]["maslow"])
            oldv = db.execute(
                "SELECT * FROM SCORES WHERE user_id = ?", session["user_id"]
            )

            score += int((oldv[0][tab]))

            db.execute(
                "UPDATE scores SET ? = ? WHERE user_id = ?",
                tab,
                score,
                session["user_id"],
            )

        # changing a booster (via post:id)
        if not sboost == None:
            target = int(
                db.execute("SELECT boost FROM tasks WHERE id=?", sboost)[0]["boost"]
            )
            if target == 0:
                db.execute("UPDATE tasks SET boost = 1 WHERE id=?", sboost)
            elif target == 1:
                db.execute("UPDATE tasks SET boost = 0 WHERE id=?", sboost)

        # render the page
        datas = create_showtask()
        return render_template("showtask.html", datas=datas)


@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    # getting basic data
    uid = session["user_id"]
    historic = db.execute("SELECT * FROM tasks WHERE user_id = ? AND closed = 1", uid)

    # if creating page via menu
    if request.method == "GET":
        # renaming
        for histo in historic:
            histo["maslow"] = maslow_word(histo["maslow"])
            histo["size"] = size_word(histo["size"])

        return render_template("history.html", historic=historic)

    # if reacitve a data
    if request.method == "POST":
        # getting the datas to be needed
        reactiv = request.form.get("back")
        task_h = db.execute("SELECT * FROM tasks WHERE id = ?", reactiv)
        score_h = score_calc(task_h[0]["maslow"], task_h[0]["size"], task_h[0]["boost"])
        cdat = "open"

        # reactivate in tasks-db
        db.execute("UPDATE tasks SET closed = 0 WHERE id=?", reactiv)
        db.execute("UPDATE tasks SET cdate = ? WHERE id=?", reactiv, cdat)

        # remove scores from scores.db
        cat_h = tab_name(task_h[0]["maslow"])
        old_h = db.execute("SELECT * FROM SCORES WHERE user_id = ?", uid)
        score_h = int((old_h[0][cat_h])) - score_h

        db.execute("UPDATE scores SET ? = ? WHERE user_id = ?", cat_h, score_h, uid)

        # refresh the page
        historic = db.execute(
            "SELECT * FROM tasks WHERE user_id = ? AND closed = 1", uid
        )
        return render_template("history.html", historic=historic)


# deleting the account and removing all datas in tasks, users and scores regarding this id
@app.route("/accdelete", methods=["GET", "POST"])
@login_required
def accdelete():
    if request.method == "GET":
        return render_template("accdelete.html")

    if request.method == "POST":
        kill_acc = request.form.get("delete")
        usid = session["user_id"]
        db.execute("DELETE FROM scores WHERE user_id = ?", usid)
        db.execute("DELETE FROM tasks WHERE user_id = ?", usid)
        db.execute("DELETE FROM users WHERE id = ?", usid)

        return redirect("/logout")


# the infopage
@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")
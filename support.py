from flask import redirect, session, render_template
from functools import wraps
from cs50 import SQL

db = SQL("sqlite:///database.db")


# returns errors within the notification-page "discard.html"
def discarder(message):
    # giving out the users fault
    return render_template("discard.html", message=message)


# checks if user is loged in
# reference to cs50x problem-set "Finance"
def login_required(f):
    # login checker
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


# returns a list, sorted on the scores
def create_showtask():
    # returns a sorted "datas-list"
    uid = session["user_id"]
    datas = db.execute("SELECT * FROM tasks WHERE user_id = ? AND closed = 0", uid)

    # starting calc and building the list
    for data in datas:
        score = score_calc(data["maslow"], data["size"], data["boost"])
        data["score"] = score

        # replacements for output
        data["maslow"] = maslow_word(data["maslow"])
        data["size"] = size_word(data["size"])

        match (data["boost"]):
            case 0:
                data["boost"] = "no"
            case 1:
                data["boost"] = "yes"

    # sort on score
    def get_score(datas):
        return datas.get("score")

    datas.sort(key=get_score, reverse=True)

    return datas


# the alogrithmen for giving the tasks there final score
def score_calc(maslow, size, boost):
    # the algorithm for scoring
    return 10 + int(maslow) - int(size) + int(boost) * 2


# replacement of the numbers regarding maslow in the database to words
def tab_name(maslow):
    # returns a tab-name for scores
    match (maslow):
        case 1:
            tabname = "selfdev"
        case 2:
            tabname = "ego"
        case 3:
            tabname = "socials"
        case 4:
            tabname = "security"
        case 5:
            tabname = "physics"

    return tabname


# alternative replacement of the numbers regarding maslow in the database to words
def maslow_word(maslow):
    # replacing numbers to words
    match (maslow):
        case 1:
            erg = "Self-actualisation"
        case 2:
            erg = "Esteem needs"
        case 3:
            erg = "Social needs"
        case 4:
            erg = "Safety needs"
        case 5:
            erg = "Physological needs"

    return erg


# replacement of the numbers regarding size in the database to words
def size_word(word):
    # replacing numbers to words
    match (word):
        case 1:
            erg = "low"
        case 2:
            erg = "medium"
        case 3:
            erg = "high"

    return erg

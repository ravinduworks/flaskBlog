from helpers import (
    sqlite3,
    session,
    request,
    redirect,
    Blueprint,
    DB_USERS_ROOT,
    render_template,
)
from delete import deleteUser

adminPanelUsersBlueprint = Blueprint("adminPanelUsers", __name__)


@adminPanelUsersBlueprint.route("/admin/users", methods=["GET", "POST"])
@adminPanelUsersBlueprint.route("/adminpanel/users", methods=["GET", "POST"])
def adminPanelUsers():
    match "userName" in session:
        case True:
            connection = sqlite3.connect(DB_USERS_ROOT)
            cursor = connection.cursor()
            cursor.execute(
                f'select role from users where userName = "{session["userName"]}"'
            )
            role = cursor.fetchone()[0]
            if request.method == "POST":
                if "userDeleteButton" in request.form:
                    deleteUser(request.form["userName"])
            match role == "admin":
                case True:
                    connection = sqlite3.connect(DB_USERS_ROOT)
                    cursor = connection.cursor()
                    cursor.execute("select * from users")
                    users = cursor.fetchall()
                    return render_template(
                        "adminPanelUsers.html",
                        users=users,
                    )
                case False:
                    return redirect("/")
        case False:
            return redirect("/")

from helpers import (
    request,
    sqlite3,
    session,
    redirect,
    Blueprint,
    DB_USERS_ROOT,
    render_template,
)
from delete import deleteUser

accountSettingsBlueprint = Blueprint("accountSettings", __name__)


@accountSettingsBlueprint.route("/accountsettings", methods=["GET", "POST"])
def accountSettings():
    match "userName" in session:
        case True:
            connection = sqlite3.connect(DB_USERS_ROOT)
            cursor = connection.cursor()
            cursor.execute(
                f'select userName from users where userName = "{session["userName"]}"'
            )
            user = cursor.fetchall()
            if request.method == "POST":
                if "userDeleteButton" in request.form:
                    deleteUser(user[0][0])
                    return redirect(f"/")
            return render_template("accountSettings.html", user=user)
        case False:
            return redirect("/login/redirect=&accountsettings")

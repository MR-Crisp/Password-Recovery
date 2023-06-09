from flask import Flask, render_template, request
from recovery import code_gen, code_checker, pass_changer, user_exist

app = Flask(__name__)


@app.get("/forget-password")
def forget_password_get():
    return render_template("forget-password.html")


@app.post("/forget-password")
def forget_password_post():
    email = request.form["email"]
    code = code_gen(email)
    if not code:
        return render_template("forget-password.html", error="Invalid username")
    return render_template("forget-password.html", success="Code has been sent")


@app.get("/confirm-code")
def confirm_code_get():
    return render_template("confirm.html")


@app.post("/confirm-code")
def confirm_code_post():
    email = request.form["email"]
    code = request.form["code"]
    if code_checker(email, code):
        return render_template("change-password.html")
    return render_template("confirm.html", error="Code is not valid")


@app.post("/change-password")
def change_password_post():
    email = request.form["email"]
    if not user_exist(email):
        return render_template("change-password.html", error="Invalid email")
    new_password = request.form["new-password"]
    confirm_password = request.form["confirm-password"]
    if new_password != confirm_password:
        return render_template("change-password.html", error="Passwords do not match")
    changed = pass_changer(email, new_password)
    if changed:
        return render_template("resolved.html")
    else:
        return render_template(
            "change-password.html", error="password did not meet requirements"
        )


if __name__ == "__main__":
    app.run()

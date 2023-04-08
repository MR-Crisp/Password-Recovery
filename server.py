from flask import Flask,render_template, request
from recovery import code_gen,code_checker,pass_changer
app = Flask(__name__)


@app.get('/forget-password')
def forget_password_get():
    return render_template('forget-password.html')

@app.post('/forget-password')
def forget_password_post():
    email = request.form["email"]
    code = code_gen(email)
    if not code:
        return render_template('forget-password.html', error="Invalid username")
    return render_template('forget-password.html', success = "Code has been sent")

@app.get('/confirm-code')
def confirm_code_get():
    return render_template('confirm.html')
    

@app.post('/confirm-code')
def confirm_code_post():
    code = request.form["code"]
    if code_checker(code):
        return render_template('change-password.html')
    return render_template("confirm.html", error = 'Code is not valid')

@app.post('/change-password')
def change_password_post():
    new_password = request.form["new_password"]
    confirm_password = request.form["confirm_password"]
    if new_password!= confirm_password:
        return render_template("change-password.html", error = "Passwords do not match")
    pass_changer(new_password)
    return render_template("change-password.html", success = "Password changed successfully")

if __name__ == '__main__':
    app.run()



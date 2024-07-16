from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "fa24l3e2l442l443k535h63jb65b7bh87bh"
db = SQLAlchemy(app)

class ToDo(db.Model):
    do_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
@app.route('/create',methods=['POST','GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']
        todo = ToDo(title=title,text=text)
        if title and text:
            db.session.add(todo)
            db.session.commit()
        return redirect(url_for('create'))
    else :
        return render_template('create.html')
@app.route('/home')
def main():
    todo = ToDo.query.all()
    return render_template('main.html',todo=todo)

@app.route('/',methods=['POST','GET'])
@app.route('/singup',methods=['POST','GET'])
def index():
    if 'user' in session:
        return redirect(url_for('main'))
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']
        users = User.query.all()
        for u in users:
            if u.login == login and u.password == password:
                print(True)
                session['user'] = login
                return redirect(url_for('main'))

        newuser = User(login=login,password=password)
        db.session.add(newuser)
        db.session.commit()
        session['user'] = login
        print(request.form)

    return render_template('index.html')



@app.route('/change/<int:id>')
def change(id):
    info = ToDo.query.get(id)
    if info:
        return render_template('change.html',info=info)
    return "GG"

@app.route('/change/<int:id>/del')
def delete(id):
    info = ToDo.query.get(id)
    try:
        db.session.delete(info)
        db.session.commit()
        return redirect(url_for('main'))
    except:
        return "Cant delete this shiet"

@app.route('/change/<int:id>/update',methods=['GET','POST'])
def update(id):
    info = ToDo.query.get(id)
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']
        info.title = title
        info.text = text
        db.session.commit()
        return redirect(f"/change/{id}")
    return render_template('update.html',info=info)



if __name__ == "__main__":
    app.run(debug=True)

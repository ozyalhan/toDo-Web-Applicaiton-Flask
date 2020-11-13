from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "flask_toDo"  # required for flash :)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/ozgur/Desktop/ozy_flask/ToDoApp/todo.db'
db = SQLAlchemy(app)

# Url mapping


@app.route("/")
def index():
    # liste döner liste içinde tüm özellikler sözlük olarak döner.
    todos = ToDo.query.all()
    return render_template("index.html", todos=todos)

# <form action="/add" method="post"> burayı tetikliyor.
# sadece post işlemleri yapmayı planlıyoruz.


@app.route("/add", methods=["POST"])
def addToDo():
    title = request.form.get("title")
    newToDo = ToDo(title=title, complete=False)  # obje
    db.session.add(newToDo)  # obje ile veri eklenmiş oldu
    db.session.commit()  # commit lendi.

    return redirect(url_for("index"))

# bu id flask tarafından gönderiliyor ?!?


@app.route("/complete/<string:id>")
def completeToDo(id):
    # first e gerek yok ama durabilir. baya baya gerek var tekli eleman sonucu ile all sonucu apayrı
    todo = ToDo.query.filter_by(id=id).first()
    # if todo.complete:
    #     todo.complete = False: #dönüşüm sağlandı.
    # else:
    #     todo.complete = True: #dönüşüm sağlandı.

    todo.complete = not todo.complete  # true ise false olur false ise true

    db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<string:id>")
def deleteToDo(id):
    del_record = ToDo.query.filter_by(id=id).first()
    db.session.delete(del_record)
    db.session.commit()
    return redirect(url_for("index"))


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    complete = db.Column(db.Boolean)


if __name__ == "__main__":
    # ilk kez tabloyu oluşturur ardından her program açıldığında tabloları oluşturmaz!
    db.create_all()
    app.run(debug=True)

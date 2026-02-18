import os
from database import db
from models import articles, users
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user ,login_required, current_user
from dotenv import load_dotenv
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask (__name__) #Inicia a aplicação flask
app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db" #Configura o tipo de banco de dados será usado
lm = LoginManager(app)
lm.login_view = "login"
db.init_app(app) #Inicia a aplicação do banco de dados

@lm.user_loader
def user_loader(id):
    user = db.session.query(users).filter_by(id=id).first()
    return user

@app.route("/") #Definição de rota
def home(): #Função a ser executada caso a rota seja acessada
    articles_data = db.session.query(articles).all() #Pegar todos os dados do bando de dados
    return render_template("index.html", articles=articles_data) #Saída da função, que é uma chamada para renderizar o index.html passando a variável articles

@app.route("/article/<int:id>")
def article(id):
    article_data = db.session.query(articles).filter_by(id=id).first()
    return render_template("article.html", article=article_data)

"""
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        name = request.form["nameForm"]
        password = request.form["passwordForm"]

        user = users(name=name, password=generate_password_hash(password), email="heytorcardosomachado@gmail.com", type="admin")
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("admin"))
"""

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin"))
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        name = request.form["nameForm"]
        password = request.form["passwordForm"]

        user = db.session.query(users).filter_by(name=name).first()
        if not user:
            return "Usuário não existe na base de dados!"
        if check_password_hash(user.password, password):
            login_user(user)
            print("Login realizado com sucesso!")
            return redirect(url_for("admin"))
        else:
            return "Senha incorreta!"

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/admin")
@login_required
def admin():
    articles_data = db.session.query(articles).all() #Pegar todos os dados do bando de dados
    return render_template("admin.html", articles=articles_data)

@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "GET":
        return render_template("create.html")
    elif request.method == "POST":
        title = request.form["titleForm"]
        sub_title = request.form["sub_titleForm"]

        article = articles(title=title, sub_title=sub_title, content="", create_date=(date.today().strftime('%d/%m/%Y')), modify_date=date.today(), likes=0, favorite=False)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for("edit", id=article.id))
    
@app.route("/article/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    article = db.session.query(articles).filter_by(id=id).first()
    if request.method == "GET":
        return render_template("edit.html", article=article)
    elif request.method == "POST":
        title = request.form["titleForm"]
        sub_title = request.form["sub_titleForm"]
        content = request.form["contentForm"]

    article.title = title
    article.sub_title = sub_title
    article.content = content
    article.modify_date = (date.today().strftime('%d/%m/%Y'))
    db.session.commit()
    return redirect(url_for("admin"))


@app.route("/article/delete/<int:id>")
@login_required
def delete(id):
    article = db.session.query(articles).filter_by(id=id).first()
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for("admin"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 2010))
    app.run(host="0.0.0.0", port=port, debug=True)
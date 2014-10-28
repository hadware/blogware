# -*- coding: utf8 -*-
from flask import Flask, url_for, session, request, render_template, redirect
from database import database, admin_logins, articles
app = Flask(__name__)

context = {}


@app.route('/admin/', methods=['POST', 'GET'])
def admin():
    """Affiche un login, sinon une page d'admin listant les posts, et proposant d'en créer de nouveaux"""
    if "admin_logged" in session and session["admin_logged"]:
        #utilisateur loggé, affichage de la page d'admin
        return redirect(url_for("admin_home"))
    else:
        if request.method == "GET":
            #displays a login form
            return render_template("admin_login.html")
        else:
            #processes the login data
            if admin_logins.find_one({"password" : request.form["password"]}):
                session["admin_logged"] = True
                return redirect(url_for("admin_home"))
            else:
                return render_template("admin_login.html", error = "Mauvais mot de passe")

@app.route("/admin/home")
def admin_home():
    """Affiche la page d'admin avec le listings des articles"""

    def build_admin_urls(article_dict):
        """Crée les liens d'administration (surpp, edit, voir)"""
        buffer_dict = article_dict
        buffer_dict.pop("content")
        buffer_dict.update({"delete_link" : url_for("article_delete", article_id = str(article_dict["_id"])),
                           "edit_link" : url_for("article_edit", article_id = str(article_dict["_id"])),
                           "view_link" : url_for("article_view", article_id = str(article_dict["_id"]))})

        return buffer_dict

    entries = [build_admin_urls(article) for article in articles.find()]
    return render_template("admin_home.html", entries = entries)

@app.route("/admin/article/delete/<article_id>")
def article_delete(article_id):
    pass

@app.route("/admin/article/edit/<article_id>")
def article_edit(article_id):
    pass

@app.route("/admin/article/view/<article_id>")
def article_view(article_id):
    pass

@app.route('/')
@app.route('/index')
def index():
    """Listing des 5 derniers posts (tous pour l'instant), en n'affichant qu'un résumé pour chacun des posts"""
    def build_article_data(article_dict):
        buffer_dict = article_dict
        #making the summary, the hard way
        buffer_dict["summary"] = buffer_dict["content"] if len(buffer_dict["content"]) <= 500 else buffer_dict["content"][0:500]
        buffer_dict["view_link"] = url_for("article_view", article_id = str(article_dict["_id"]))
        return buffer_dict
    context["entries"] = [build_article_data(article) for article in articles.find()]
    return render_template("home.html", context=context)


@app.route('/article/<article_id>/')
def display_article(article_id):
    """Displays a single article"""
    pass

if __name__ == '__main__':
    app.debug = True
    app.run()
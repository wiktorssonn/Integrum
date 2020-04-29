from flask import render_template, request, Blueprint
from flask_integrum.models import Post

main = Blueprint("main", __name__)



@main.route("/hem")
def hem():
    return render_template("index.html")



@main.route("/ia")
def ia():
    return render_template("ia.html", title="Informationsarkitekt")



@main.route("/schema")
def schema():
    return render_template("schema.html", title="Schema")



@main.route("/calendar")
def calendar():
    return render_template("calendar.html", title="Calendar")



@main.route("/om_oss")
def om_oss():
    return render_template("om_oss.html", title="Om Oss")



@main.route("/kontakt")
def kontakt():
    return render_template("kontakt.html", title="Kontakt")



@main.route("/forum")
def forum():
    #Sätter sida 1 till default, försöker man ange något annat än en int blir det ValueError.
    page = request.args.get("page", 1, type=int)
    #Hämtar inlägg från databasen och sorterar efter senaste datum, paginate ger oss möjlighet att styra hur många inlägg som ska visas per sida etc.
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("forum.html", title="Forum", posts=posts)
    


@main.route("/faq")
def faq():
    return render_template("faq.html", title="FAQ")



@main.route("/todo")
def todo():
    return render_template("todo.html", title="Att göra")



@main.route("/uppgift")
def uppgift():
    return render_template("uppgift.html", title="Uppgift")
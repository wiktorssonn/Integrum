from flask import (render_template, request, Blueprint, jsonify, flash,
                    redirect, url_for)
from flask_login import login_required, current_user
from flask_integrum import db
from flask_integrum.models import Post, Todo
from flask_integrum.posts.forms import PostForm
import requests
from bs4 import BeautifulSoup
from flask_integrum.main.forms import PostAssignment



main = Blueprint("main", __name__)


@main.route("/schema")
def schema():
    year1 = request.args.get('resurser', 'p.TGIAA19h')
    year2 = request.args.get('resurser', 'p.TGIAA18h')
    year3 = request.args.get('resurser', 'p.TGIAA17h')
    
    url_test = 'https://schema.mau.se/setup/jsp/Schema.jsp?startDatum=idag&intervallTyp=m&intervallAntal=6&sprak=SV&sokMedAND=true&forklaringar=true&resurser={}'.format(year1)
    url = 'https://schema.mau.se/setup/jsp/Schema.jsp?startDatum=idag&intervallTyp=m&intervallAntal=6&sprak=SV&sokMedAND=true&forklaringar=true&resurser=p.TGIAA19h'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    schema = soup.select(".schemaTabell .data-grey, .schemaTabell .data-white")
    schema_data = []
    for i, row in enumerate(schema):
        row_data = [child for child in row.children]
        num_cols = len(row_data)
        print(row_data[7].string)
        print(row_data[8].string)
        print(row_data[9].string)
        print(row_data[10].string)
        print(row_data[11].string)
        if num_cols == 11:

            day = row_data[2].string.replace(u"\xa0", "")
            date = row_data[3].string.replace(u"\xa0", "")

            if day == "" and date == "":
                prev_row_data = [child for child in schema[i - 1].children]
                day = prev_row_data[2].string.replace(u"\xa0", "")
                date = prev_row_data[3].string.replace(u"\xa0", "")

            time = row_data[4].string.replace(u"\xa0", "")
            course = "".join([c.string for c in row_data[5].children]).replace(u"\xa0", "")
            teacher = "".join([t.string for t in row_data[6].children]).replace(u"\xa0", "")
            room = "".join([r.string for r in row_data[7].children]).replace(u"\xa0", "")
            resource = row_data[8].string.replace(u"\xa0", "")
            moment = row_data[9].string.replace(u"\xa0", "")
            updated = row_data[10].string.replace(u"\xa0", "")

            data = {
                "day": day,
                "date": date,
                "time": time,
                "course": course,
                "teacher": teacher,
                "room": room,
                "resource": resource,
                "moment": moment,
                "updated": updated
            }

            schema_data.append(data)
        else:
            day = row_data[2].string.replace(u"\xa0", "")
            date = row_data[3].string.replace(u"\xa0", "")

            if day == "" and date == "":
                prev_row_data = [child for child in schema[i - 1].children]
                day = prev_row_data[2].string.replace(u"\xa0", "")
                date = prev_row_data[3].string.replace(u"\xa0", "")
            time = row_data[4].string.replace(u"\xa0", "")
            course = "".join([c.string for c in row_data[5].children]).replace(u"\xa0", "")
            group = "".join([g.string for g in row_data[6].children]).replace(u"\xa0", "")
            teacher = "".join([t.string for t in row_data[7].children]).replace(u"\xa0", "")
            room = "".join([r.string for r in row_data[8].children]).replace(u"\xa0", "")
            resource = row_data[9].string.replace(u"\xa0", "")
            moment = row_data[10].string.replace(u"\xa0", "")
            updated = row_data[11].string.replace(u"\xa0", "")

            data = {
                "day": day,
                "date": date,
                "time": time,
                "course": course,
                "group": group,
                "teacher": teacher,
                "room": room,
                "resource": resource,
                "moment": moment,
                "updated": updated
            }

            schema_data.append(data)
    
    # En rad
    # return jsonify(schema_data)
    return render_template("schema.html", schema=schema_data, title="Schema")

    # JSON
    # print(json.dumps(schema_data))


@main.route("/hem")
def hem():
    # Sätter sida 1 till default, försöker man ange något annat än en
    # int blir det ValueError.
    page = request.args.get("page", 1, type=int)
    # Hämtar inlägg från databasen och sorterar efter senaste datum
    # paginate ger oss möjlighet att styra hur många inlägg som ska visas per sida etc.
    
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template("index.html", posts=posts)



@main.route("/ia")
def ia():
    return render_template("ia.html", title="Informationsarkitekt")


@main.route("/calendar")
def calendar():
    return render_template("calendar.html", title="Calendar")



@main.route("/om_oss")
def om_oss():
    return render_template("om_oss.html", title="Om Oss")



@main.route("/kontakt")
def kontakt():
    return render_template("kontakt.html", title="Kontakt")



@main.route("/forum", methods=["GET", "POST"])
def forum():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Ditt inlägg har publicerats!", "success")
        return redirect(url_for("main.forum"))


    #Sätter sida 1 till default, försöker man ange något annat än en int blir det ValueError.
    page = request.args.get("page", 1, type=int)
    #Hämtar inlägg från databasen och sorterar efter senaste datum, paginate ger oss möjlighet att styra hur många inlägg som ska visas per sida etc.
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("forum.html", title="Forum", posts=posts, form=form, legend="Nytt inlägg")



@main.route("/todo", methods=["GET", "POST"])
def todo():
    task = PostAssignment()
    if task.validate_on_submit():
        task = PostAssignment()
        assignment = Todo(assignment=task.title.data, description=task.description.data, assignment_author=current_user)
        db.session.add(assignment)
        db.session.commit()
        flash("En ny uppgift har skapats!", "Din lista har blivit uppdaterad!")
        return redirect(url_for("main.todo"))
    #assignments = Todo.query.all(
    assignments = Todo.query.filter_by(user_id=assignment_author)
    #ASSIGMENT AUTHOR FUCKAR
    return render_template("todo.html", title="Att göra", task=task, assignments=assignments, legend="Lägg till ny uppgift")


    
@main.route("/faq")
def faq():
    return render_template("faq.html", title="FAQ")



@main.route("/uppgift")
def uppgift():
    return render_template("uppgift.html", title="Uppgift")

   


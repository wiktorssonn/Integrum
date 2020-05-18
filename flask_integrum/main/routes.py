from flask import (render_template, request, Blueprint, jsonify, flash,
                    redirect, url_for)
from flask_login import login_required, current_user
from flask_integrum import db
from flask_integrum.models import Post, Todo
from flask_integrum.posts.forms import PostForm
from bs4 import BeautifulSoup
import requests
from flask_integrum.main.forms import PostAssignment



main = Blueprint("main", __name__)



def fix_row_data(row):
    if row.string is None:
        return "".join([r.string if r.string is not None else "" for r in row.contents]).replace(u"\xa0", "")           
    else: 
        return row.string.replace(u"\xa0", "")



@main.route("/schema")
def schema():
    year = request.args.get('resurser', 'p.TGIAA19h')
    
    
    url = 'https://schema.mau.se/setup/jsp/Schema.jsp?startDatum=idag&intervallTyp=m&intervallAntal=6&sprak=SV&sokMedAND=true&forklaringar=true&resurser={}'.format(year)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    schema = soup.select(".schemaTabell .data-grey, .schemaTabell .data-white")
    schema_data = []
    for i, row in enumerate(schema):
        row_data = [child for child in row.children]
        num_cols = len(row_data)
    
        if num_cols == 11:
            
            # Kallar på funktionen fix_row_data() med respektive index(kolumn) från kronox
            data = {
                "day": fix_row_data(row_data[2]),
                "date": fix_row_data(row_data[3]),
                "time": fix_row_data(row_data[4]),
                "course": fix_row_data(row_data[5]),
                "teacher": fix_row_data(row_data[6]),
                "room": fix_row_data(row_data[7]),
                "resource": fix_row_data(row_data[8]),
                "moment": fix_row_data(row_data[9]),
                "updated": fix_row_data(row_data[10])
            }

            schema_data.append(data)
        else:
            
            data = {
                "day": fix_row_data(row_data[2]),
                "date": fix_row_data(row_data[3]),
                "time": fix_row_data(row_data[4]),
                "course": fix_row_data(row_data[5]),
                "group": fix_row_data(row_data[6]),
                "teacher": fix_row_data(row_data[7]),
                "room": fix_row_data(row_data[8]),
                "resource": fix_row_data(row_data[9]),
                "moment": fix_row_data(row_data[10]),
                "updated": fix_row_data(row_data[11])
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
    url = 'https://edu.mau.se/sv/program/tgiaa'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    utb_data=[]


    utb_plan = soup.select('.edu-plan__term, .edu-plan__description')
    lista=[]

    for i in utb_plan:
        i = i.text
        i = i.strip(' ')

        lista.append(i)


    # Sparar variablerna i ett dict
    data = {
        "Programkod": lista[0],
        "Data1": lista[1],
        "Engelsk_benämning": lista[2],
        "Data2": lista[3],
        "Undervisningsspråk": lista[4],
        "Data3": lista[5],
        "Inrättandedatum": lista[6], 
        "Data4": lista[7],
        "Fastställandedatum": lista[8],
        "Data5": lista[9],
        "Beslutande_instans": lista[10],
        "Data6": lista[11],
        "Gäller_från": lista[12],
        "Data7": lista[13],
        "Ersätter": lista[14],
        "Data8": lista[15],
    }

    utb_data.append(data)

    return render_template("ia.html", tabledata=utb_data, title="Informationsarkitekt")


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



#Lägg till upggiften till "att-göra" listan
@main.route("/add_todo", methods=["POST"])
def add_todo():
    task = PostAssignment()
    if task.validate_on_submit():
        todo = Todo(assignment=task.assignment.data, description=task.description.data, completed=False, user_id=current_user.id)
        db.session.add(todo)
        db.session.commit()
        flash("En ny uppgift har skapats!", "success")
        return redirect(url_for("main.todo"))
    
    return render_template("todo.html", title="Att göra", legend="Lägg till ny uppgift", task=task)



#Ta bort uppgift från "att-göra" listan
@main.route("/delete_todo/<id>")
def delete_todo(id):
    
    #Tar bort uppgiften med id:et man klickat på i "att-göra" listan från databasen
    todo = Todo.query.filter_by(id=int(id)).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for("main.todo"))
    


#"Att-göra" listan där man kan lägga till uppgifter som ska göras
@main.route("/todo")
def todo():
    task = PostAssignment()
    #Hämtar ut alla assignments som tillhör current_user, alltså kollar att user_id i databasen == current_user
    assignments = Todo.query.filter(Todo.user_id == current_user.id).all()
    return render_template("todo.html", title="Att göra", assignments=assignments, task=task)




    
@main.route("/faq")
def faq():
    return render_template("faq.html", title="FAQ")



@main.route("/uppgift")
def uppgift():
    return render_template("uppgift.html", title="Uppgift")

   


from flask import render_template, request, Blueprint, jsonify
from flask_integrum.models import Post
import requests
from bs4 import BeautifulSoup

main = Blueprint("main", __name__)


@main.route("/schema.json")
def json_schema():
    url = 'https://schema.mau.se/setup/jsp/Schema.jsp?startDatum=idag&intervallTyp=m&intervallAntal=6&sprak=SV&sokMedAND=true&forklaringar=true&resurser=p.TGIAA17h'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    schema = soup.select(".schemaTabell .data-grey, .schemaTabell .data-white")
    schema_data = []

    for i, row in enumerate(schema):
        row_data = [child for child in row.children]

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

    # En rad
    return jsonify(schema_data)

    # JSON
    # print(json.dumps(schema_data))


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
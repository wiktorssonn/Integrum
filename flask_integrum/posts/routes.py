from flask import (render_template, url_for, flash, redirect,
                    request, abort, Blueprint)
from flask_login import current_user, login_required
from flask_integrum import db
from flask_integrum.models import Post
from flask_integrum.posts.forms import PostForm


posts = Blueprint("posts", __name__)



@posts.route("/create_post", methods=["GET","POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Ditt inlägg har publicerats!", "success")
        return redirect(url_for("main.forum"))
    return render_template("create_post.html", title="Nytt inlägg", form=form, legend="Nytt Inlägg")



#Varje post får en unik sökväg
@posts.route("/post/<int:post_id>")
def post(post_id):
    #Om sökvägen inte finns, returnera 404
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)



#Uppdatera inlägg
@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    #Om sökvägen inte finns, returnera 404
    post = Post.query.get_or_404(post_id)
    #Om skaparen av inlägget inte är inloggad användare, raise felmeddelande
    if post.author != current_user:
        abort(403)
    form = PostForm()
    #Om uppdateringen validerar, uppdatera inlägg
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Inlägget har uppdaterats!", "success")
        return redirect(url_for("posts.post", post_id=post.id))
    elif request.method == "GET":
        #Fyller i fälten med texten som finns i nuläget
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", title="Update Post", form=form, legend="Uppdatera Inlägg")



#Ta bort inlägg
@posts.route("/post/<int:post_id>/delete", methods=["GET", "POST"])
@login_required
def delete_post(post_id):
    #Om sökvägen inte finns, returnera 404
    post = Post.query.get_or_404(post_id)
    #Om skaparen av inlägget inte är inloggad användare, raise felmeddelande
    if post.author != current_user:
        abort(403)
    #Tar bort inlägget
    db.session.delete(post)
    db.session.commit()
    flash("Ditt inlägg är borttaget!", "success")
    return redirect(url_for("main.forum"))
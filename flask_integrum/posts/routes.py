from flask import (render_template, url_for, flash, redirect,
                    request, abort, Blueprint)
from flask_login import current_user, login_required
from flask_integrum import db
from flask_integrum.models import Post
from flask_integrum.posts.forms import PostForm



posts = Blueprint("posts", __name__)



#Varje post får en unik sökväg
@posts.route("/post/<int:post_id>")
def post(post_id):
    #Om sökvägen inte finns, returnera 404
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", 
                            title=post.title, 
                            post=post)



#Uppdatera inlägg
@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    #Om sökvägen inte finns, returnera 404
    post = Post.query.get_or_404(post_id)

    #Om skaparen av inlägget inte är inloggad, raise felmeddelande
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
    
    '''
    Sätter sida 1 till default, försöker man ange
    något annat än en int blir det ValueError.
    '''

    page = request.args.get("page", 1, type=int)

    '''
    Hämtar inlägg från databasen och sorterar efter senaste datum.
    Paginate ger oss möjlighet att styra hur många 
    inlägg som ska visas per sida etc.
    '''

    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,
                                                                 per_page=5)
    return render_template("update_post.html", 
                            title="Update Post",   
                            form=form, 
                            posts=posts, 
                            legend="Uppdatera Inlägg")



#Ta bort inlägg
@posts.route("/post/<int:post_id>/delete", methods=["GET", "POST"])
@login_required
def delete_post(post_id):

    #Om sökvägen inte finns, returnera 404
    post = Post.query.get_or_404(post_id)

    #Om skaparen av inlägget inte är inloggad, raise felmeddelande
    if post.author != current_user:
        abort(403)
        
    #Tar bort inlägget
    db.session.delete(post)
    db.session.commit()
    flash("Ditt inlägg är borttaget!", "success")
    return redirect(url_for("main.forum"))
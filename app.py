from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#My app
app = Flask(__name__)
Scss(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()
class stask(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(100), nullable = False)
    complete = db.Column(db.Integer)
    created = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"Task {self.id}"

@app.route("/",methods = ["POST", "GET"])
def index():
    #Add task
    if request.method == "POST":
        current_task = request.form['content']
        new_task = stask(content = current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Error detected: {e}")
            return f"Error: {e}"
    #See all current tasks
    else:
        tasks = stask.query.order_by(stask.created).all()
    return render_template("index.html", tasks=tasks)




@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = stask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"Error:{e}"
@app.route("/update/<int:id>", methods = ["GET", "POST"])   
def update(id:int):
    update_task = stask.query.get_or_404(id)
    if request.method == "POST":
        update_task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Error {e}"
    else:
        return render_template("edit.html", task = update_task)








if __name__  == "__main__":

    app.run(debug = True)
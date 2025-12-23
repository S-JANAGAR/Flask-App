import sqlite3
from flask import Flask,render_template,request # type: ignore

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/addContact")
def add():
    return render_template("addContact.html")

@app.route("/saveDetials",methods=["POST"])
def saveDetials():
    msg=""
    if request.method=="POST":
        try:
            name = request.form.get("name")
            email = request.form.get("email")
            phone_no = request.form.get("phone_no")
            address = request.form.get("address")
            with sqlite3.connect("Contact.db") as con:
                crur=con.cursor()
                crur.execute("insert into Contact_List(Name,Email,Phone_no,Address) values (?,?,?,?)",(name,email,phone_no,address))
                con.commit()
                msg="Contact  successfully Added"
        except:
            con.rollback()
            msg="Cn't Add Contact to the List"
        finally:
            con.close() 
            return render_template("success.html",msg=msg)
            

@app.route("/viewContact")
def view():
    con=sqlite3.connect("Contact.db")
    con.row_factory=sqlite3.Row
    crur=con.cursor()
    crur.execute("select * from Contact_List")
    rows =crur.fetchall()
    return render_template("viewContact.html",rows=rows)

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/searchContact",methods=["POST"])
def searchrecord():
    if request.method=="POST":
        id=request.form.get("id")
        rows=[]
        try:
            with sqlite3.connect("Contact.db") as con:
                con.row_factory=sqlite3.Row
                crur=con.cursor()
                crur.execute("select * from Contact_List where Id=?",id)
                rows =crur.fetchall()
                if not rows:
                    msg="No such Contact Found from the Contact List"
                else:    
                    msg="Contact Found from the Contact List"
        except Exception as e:
            msg=str(e)
        finally:
            return render_template("searchContact.html",msg=msg,rows=rows) 

@app.route("/delete")
def delete():
    return render_template("delete.html")


@app.route("/deleteContact",methods=["POST"])
def deleterecord():
    msg=""
    if request.method=="POST":
        id=request.form["id"]
        try:
            with sqlite3.connect("Contact.db") as con:    
                crur=con.cursor()
                crur.execute("select * from Contact_List where Id=?",id)
                rows =crur.fetchall()
                if rows:
                    crur.execute("delete from Contact_List where Id=?",id)
                    msg="Contact successfully deleted from the contact List"
                else:
                    msg="Can't delete Contact from the contact List"
        except Exception as e:
            msg=str(e) 
        finally: 
            return render_template("deleteContact.html",msg=msg)  
                

if __name__=="__main__":
    app.run(debug=True)        
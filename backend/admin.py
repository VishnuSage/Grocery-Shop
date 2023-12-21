from flask import Flask, render_template,request , redirect, url_for, session,flash
import os
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import mysql.connector
import MySQLdb.cursors
import re





app = Flask(__name__)
connection = mysql.connector.connect(host="localhost",user="root",password="",database="grocery")
mycursor = connection.cursor()

UPLOAD_FOLDER = os.path.join('static', 'uploads')
# # Define allowed files
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] =UPLOAD_FOLDER

app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'grocery'
  
mysql = MySQL(app)






@app.route("/")
def getadminlogin():
    return render_template("/loginadmin.html")

@app.route('/loginadmin', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form :
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM login WHERE username = % s AND password = % s AND usertype ='admin'", (username, password ))
        user = cursor.fetchone()
        if user:
            mesage = 'Logged in successfully !'
            return render_template('home.html', mesage = mesage)
        else:    
            mesage = 'Please enter correct username / password !'
            return render_template('loginadmin.html', mesage = mesage)

@app.route("/logoutadmin")
def getadminloginout():
    return render_template("/loginadmin.html")

@app.route('/read', methods =['GET', 'POST'])
def add():
    if request.method =="POST":
        iname = request.form.get('iname')
        category = request.form.__getitem__('category')
        price = request.form.get('price')
        
        Quantity = request.form.get('Quantity')
        Description = request.form.get('Description') 
        
        # Upload file flask
        uploaded_img = request.files['uploaded-file']
        # Extracting uploaded data file name
        img_filename = secure_filename(uploaded_img.filename)
        # Upload file to database (defined uploaded folder in static path)
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        # Storing uploaded file path in flask session
        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
        
        query= "INSERT INTO `stock`(`iname`, `category`, `price`, `Quantity`, `Description`,`image`) VALUES (%s,%s,%s,%s,%s,%s)"
        data = (iname,category,price,Quantity,Description,img_filename)
        
     
       
        mycursor.execute(query,data)
        connection.commit()

        message = 'Stock entered Succesfully!'
        query = "SELECT * FROM `category` "
        mycursor.execute(query)
        sresult=mycursor.fetchall()

        return render_template('add.html' ,message = message,cdata=sresult)
#............................................Product Stock
  
@app.route('/add',)
def add1():
    query = "SELECT * FROM `category` "
    mycursor.execute(query)
    sresult=mycursor.fetchall()
    return render_template("/add.html",cdata=sresult)


@app.route('/Stockdetails', methods =['GET', 'POST'])
def Stockdetails():
    stk = request.form.get('stk')
    query = "SELECT `itemid`, `iname`, `cname`, `price`,`Quantity`,`Description`,`image`,`pstatus` FROM `stock` inner join `category` on category.cid = stock.category"
    if stk:
        query += " WHERE `Quantity` < {}".format(stk)
    mycursor.execute(query)
    sresult=mycursor.fetchall()
    return render_template("/Stockdetails.html",proddata=sresult)


# -----------------------sort----------------------


# --------sort end---------------------
    


@app.route('/shipping', methods =['GET', 'POST'])
def shipping():
    query = "SELECT * FROM `shipping`"
    mycursor.execute(query)
    shp=mycursor.fetchall()
    return render_template("shipping.html",shp=shp)

@app.route('/readsup', methods =['GET', 'POST'])
def supplier():
     if request.method =="POST":
        sname = request.form.get('sname')
        address = request.form.get('address')
        contact = request.form.get('contact')
        query= "INSERT INTO `supplier`(`sname`, `contact`, `address`) VALUES (%s,%s,%s)"
        data = (sname,contact,address)
        mycursor.execute(query,data)
        connection.commit()
        message = 'Succesfully added'
        return render_template('supplier.html' ,message = message)
    
@app.route('/readcat', methods =['GET', 'POST'])
def category():
     if request.method =="POST":
        cname = request.form.get('cname')
        query= "INSERT INTO `category` (`cname`) VALUES ('"+cname+ "')"
        print(query)
        mycursor.execute(query)
        connection.commit()

        message = 'Succesfully added'
        query = "SELECT * FROM `category` "
        mycursor.execute(query)
        sresult=mycursor.fetchall()
        return render_template('/category.html',catdata=sresult)   

@app.route('/supplier')
def getsup():
    return render_template('supplier.html')   

@app.route('/category')
def getcat():
    query = "SELECT * from `category` "
    mycursor.execute(query)
    sresult=mycursor.fetchall()
    return render_template('/category.html',catdata=sresult)


# start of stock edit----------------------------------------------------------------

# @app.route('/deletee/<string:itemid>', methods = ['GET'])
# def delete(itemid):
#     flash("Record Has Been Deleted Successfully")
#     cur = mysql.connection.cursor()
#     cur.execute("Update stock set status='INACTIVE' WHERE itemid=%s", (itemid,))
#     mysql.connection.commit()
    
    
#     return redirect(url_for('Stockdetails'))

@app.route('/deleteprod/<string:itemid>')
def deletee(itemid):
    query = "update stock set `pstatus`='INACTIVE' where `itemid`="+itemid
    mycursor.execute(query)
    connection.commit()
    
    query = "SELECT `itemid`, `iname`, `cname`, `price`,`Quantity`,`Description`,`image`,`pstatus` FROM `stock` inner join `category` on category.cid = stock.category "
    mycursor.execute(query)
    sresult=mycursor.fetchall()
    return render_template("/Stockdetails.html",proddata=sresult)

# .......................start of product edit button------------------

@app.route('/editprod/<string:itemid>')
def editstudent(itemid):
    query ="SELECT `itemid`, `iname`, `cname`, `price`,`Quantity`,`Description`,`image`,`pstatus` FROM `stock` inner join `category` on category.cid = stock.category where `itemid`="+itemid
    mycursor.execute(query)
    sresult=mycursor.fetchall()
    print(sresult)
    
    query = "SELECT * FROM `category` "
    mycursor.execute(query)
    cresult=mycursor.fetchall()
    return render_template("/productupdate.html",proddata=sresult,cdata=cresult) 
# end------------------------------------------------------------------------------

@app.route('/productupdate/<string:itemid>', methods=['GET', 'POST'])
def updatestudent(itemid):
    if request.method=="POST":  
        uploaded_img = request.files['uploaded-file']
        sn=request.form.get("iname")
        category=request.form.__getitem__("category")
        price=request.form["price"]
        
        st=request.form.get("pstatus")
        Quantity=request.form.get("Quantity")
        Description=request.form.get("Description")
        img_org=request.form.get("img_original")
        print(uploaded_img)
        
        if uploaded_img.filename == '':
            query = "update `stock` set `iname`=%s,`category`=%s,`price`=%s,`Quantity`=%s,`Description`=%s,`image`=%s,`pstatus`=%s where `itemid`=%s"
            data=(sn,category,price,Quantity,Description,img_org,st,itemid)
            mycursor.execute(query,data)
            connection.commit()
        else:
            img_filename = secure_filename(uploaded_img.filename)
            uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
            session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'],img_filename)
            query = "update `stock` set `iname`=%s,`category`=%s,`price`=%s,`Quantity`=%s,`Description`=%s,`image`=%s,`pstatus`=%s where `itemid`=%s"
            data=(sn,category,price,Quantity,Description,img_org,st,itemid)
            mycursor.execute(query,data)
            connection.commit()

        query = "SELECT `itemid`, `iname`, `cname`, `price`, `Quantity`,`Description`,`image`,`pstatus` FROM `stock` inner join `category` on category.cid = stock.category "
        mycursor.execute(query)
        sresult=mycursor.fetchall()
        return render_template("/Stockdetails.html",proddata=sresult)
    
    
# --------------------------------supplier start----------------------------------
@app.route('/Viewsup', methods =['GET', 'POST'])
def Viewsup():
    query = "SELECT `sid`, `sname`, `contact`, `address`,`sstatus` FROM `supplier`"
    mycursor.execute(query)
    sresult=mycursor.fetchall()
    return render_template("/Viewsup.html",supdata=sresult)
    
#   ------------------------edit sup----------------
@app.route('/editsup/<string:sid>')
def editsup(sid):
    query ="SELECT `sid`, `sname`, `contact`, `address`,`sstatus` FROM `supplier` where `sid`="+sid
    mycursor.execute(query)
    sresult=mycursor.fetchall()
    print(sresult)
    
   
    mycursor.execute(query)
    cresult=mycursor.fetchall()
    return render_template("/supupdate.html",supdata=sresult,cdata=cresult) 
# -------------------------------------end--------------------

# -------------------update sup---------------------------
@app.route('/supupdate/<string:sid>', methods=['GET', 'POST'])
def supupdate(sid):
    if request.method=="POST":  
       
        sn=request.form.get("sname")
        contact=request.form.get("contact")
        address=request.form["address"]
        st=request.form.get("sstatus")
        
        query = "update `supplier` set `sname`=%s,`contact`=%s,`address`=%s,`sstatus`=%s where `sid`=%s"
        data=(sn,contact,address,st,sid)
        mycursor.execute(query,data)
        connection.commit()
        return redirect(url_for('Viewsup'))

    query = "SELECT `sid`, `sname`, `contact`, `address`,`sstatus` FROM `supplier`"
    mycursor.execute(query)
    sresult=mycursor.fetchall()
    return render_template("/Viewsup.html",supdata=sresult)
    
    # ----------------end-----------------------------------------------------------------
   
#    ------------------------delete sup -------------------------
@app.route('/deletesup/<string:sid>')
def deletesup(sid):
    query = "update supplier set `sstatus`='INACTIVE' where `sid`="+sid
    mycursor.execute(query)
    connection.commit()
    
    query = "SELECT `sid`, `sname`, `contact`, `address`,`sstatus` FROM `supplier`"
    mycursor.execute(query)
    sresult=mycursor.fetchall()
    return render_template("/Viewsup.html",supdata=sresult)

# ---------------------end-------------------------------------------

# @app.route('/orders', methods =['GET', 'POST'])
# def orders():
    
#     query = "SELECT `iname`,orders.quantity,orders.price,`order_date`,orders.item_id,orders.id,orders.status FROM `orders` ,`stock` where `orders`.`item_id`=`stock`.`itemid`"
#     mycursor.execute(query)
#     orders=mycursor.fetchall()
    
   
#     return render_template("/orderdisp.html",odata=orders)

# -------------------------sort start-------------------

@app.route('/orders', methods=['GET', 'POST'])
def orders():
    from_date = request.form.get('fdate')
    to_date = request.form.get('tdate')
    print(from_date,to_date)
    query = "SELECT `iname`, orders.quantity, orders.price, `order_date`, orders.item_id, orders.orderid, orders.status FROM `orders`, `stock` WHERE `orders`.`item_id` = `stock`.`itemid`"
    
    if from_date and to_date:
        query += " AND `order_date` BETWEEN '{}' AND '{}'".format(from_date, to_date)
    query += " ORDER BY `order_date` DESC"
    mycursor.execute(query)
    orders = mycursor.fetchall()
    return render_template("/orderdisp.html", odata=orders)


# sort end------------------------------

# ------------------------ordermdisp accept button and decline button start--------------

@app.route('/accept/<string:item_id>/<string:quantity>/<string:id>')
def accept(item_id,quantity,id):
 

    sql = "UPDATE stock SET stock.Quantity = stock.Quantity - %s  WHERE stock.itemid = %s"
    values = (quantity, item_id)
    query = "update orders set `status`='Accepted' where `id`="+id
    mycursor.execute(query)
    query = "SELECT `iname`,orders.quantity,orders.price,`order_date`,orders.item_id,orders.id,orders.status FROM `orders` ,`stock` where `orders`.`item_id`=`stock`.`itemid`"
    query += " ORDER BY `order_date` DESC"   
    mycursor.execute(query)
    orders=mycursor.fetchall()
    mycursor.execute(sql, values)
    connection.commit()
    return render_template("/orderdisp.html",odata=orders)
    
# ----------------------------------end-----------------------------------------
# ---------------------------order decline button start----------------

@app.route('/decline/<string:id>')
def decline(id):
    query = "update orders set `status`='Declined' where `id`="+id
    mycursor.execute(query)
    connection.commit()
    
    query = "SELECT `iname`,orders.quantity,orders.price,`order_date`,orders.item_id,orders.id,orders.status FROM `orders` ,`stock` where `orders`.`item_id`=`stock`.`itemid`"
    mycursor.execute(query)
    orders=mycursor.fetchall()
    connection.commit()

    return render_template("/orderdisp.html",odata=orders)

# ---------------------end-----------------------------------------------




if __name__ =='__main__':
    app.run(debug="True")
     
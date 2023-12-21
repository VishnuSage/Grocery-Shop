from flask import Flask, render_template,request,session,redirect,url_for
import os
from flask_mysqldb import MySQL
import mysql.connector
import MySQLdb.cursors
import re


app = Flask(__name__ )




connection = mysql.connector.connect(host="localhost",user="root",password="",database="grocery")

mycursor = connection.cursor()
app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'grocery'
  
mysql = MySQL(app)


@app.route("/")
def home():
    mycursor.execute("SELECT * FROM stock ORDER BY RAND() LIMIT 4;")
    rows = mycursor.fetchall()
    return render_template('index2.html', products=rows, )

    

@app.route("/index2")
def index2():
    mycursor.execute("SELECT * FROM stock ORDER BY RAND() LIMIT 4;")
    rows = mycursor.fetchall()
    return render_template('index2.html', products=rows, )
    

@app.route("/index3")
def index3():
    mycursor.execute("SELECT * FROM stock ORDER BY RAND() LIMIT 4;")
    rows = mycursor.fetchall()
    return render_template('index3.html', products=rows, )
    
   
@app.route("/logout")
def logout():
    session.clear()
    
    return redirect("/index2")

    


   

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM login WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user:
            session['logged_in'] = True
          
            session['username'] = user['username']
            message = 'Logged in successfully!'
            return redirect(url_for('shop'))
        else:
            message = 'Invalid login credentials!'
    return render_template('login.html', message=message)




    

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cpassword = request.form['cpassword']
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        pin = request.form['pin']
        state = request.form['state']
        district = request.form['district']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM login WHERE username = %s", (username,))
        account = cursor.fetchone()
        if account:
            message = 'Account already exists!'
        elif not username or not password:
            message = 'Please fill out the form!'
        elif password != cpassword:
            message = 'Passwords do not match!'
        else:
            cursor.execute("INSERT INTO login(username, password) VALUES(%s, %s)", (username, password))
            cursor.execute("INSERT INTO userdetails(username,name,address,phone,pin,state,district) VALUES(%s, %s,%s,%s,%s,%s,%s)", (username,name,address,phone,pin,state,district ))
            mysql.connection.commit()
           
            message = 'You have successfully registered!'
            return redirect(url_for('login'))
    return render_template('signin.html', message=message)




# @app.route('/userdetails', methods=['GET', 'POST'])
# def userdetails():
#     if request.method == "POST":
#         name = request.form.get('name')
#         address = request.form.get('address')
#         phone = request.form.get('phone')
#         pin = request.form.get('pin')
#         state = request.form.get('state')
#         district = request.form.get('district')

#         query = "UPDATE userdetails SET name=%s, address=%s, phone=%s, pin=%s, state=%s, district=%s WHERE id=%s"
#         data = (name, address, phone, pin, state, district, session['user_id'])

#         mycursor.execute(query, data)
#         mysql.connection.commit()

#         message = 'Succesfully signed in'
#         return render_template('login.html', message=message)
    
#     return render_template('userdetails.html', )




# ---------------------------Product start here-------------------------------------
@app.route('/shop')
def shop():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    else:
        username = session['username']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM login WHERE username = %s", (username,))
        user = cursor.fetchone()
        mycursor.execute("SELECT * FROM stock,category where category.cid=stock.category and stock.pstatus='ACTIVE'")
        rows = mycursor.fetchall()
        return render_template('shop.html', products=rows, user=user)

# @app.route('/logout1')
# def logout1():
#     session.clear()
#     return redirect(url_for('index2'))

# ------------for category--------------------------
@app.route('/veg')
def veg():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    else:
        username = session['username']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM login WHERE username = %s", (username))
        user = cursor.fetchone()
        mycursor.execute("SELECT * FROM stock,category where category.cid=stock.category and stock.category='2'")
        rows = mycursor.fetchall()
        return render_template('shop.html', products=rows, user=user)
# -------------------fruits--------------------------------------------------
@app.route('/fru')
def fru():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    else:
        username = session['username']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM login WHERE username = %s", (username))
        user = cursor.fetchone()
        mycursor.execute("SELECT * FROM stock,category where category.cid=stock.category and stock.category='1'")
        rows = mycursor.fetchall()
        return render_template('shop.html', products=rows, user=user)

# --------------end------------
#--------------------------cart start-----------------------------------------
import secrets
# Generate a secure random order ID


@app.route('/add', methods=['POST'])
def addcart():
    quantity = int(request.form['quantity'])
    itemid = int(request.form['itemid'])

    # validate the received values
    if quantity and itemid and request.method == 'POST':
        query = "SELECT * FROM stock WHERE itemid = %s"
        mycursor.execute(query, (itemid,))
        row = mycursor.fetchone()
        un=session['username']
        print(un)

        if row:
            item = {'iname': row[1], 'itemid': row[0], 'quantity': quantity, 'price': row[3], 'image': row[6], 'username': un}
            print(item)
            if 'cart' not in session:
                session['cart'] = []
            else:
                for i, cart_item in enumerate(session['cart']):
                    if cart_item['itemid'] == itemid :
                        session['cart'][i]['quantity'] += quantity
                        session.modified = True
                        return redirect(url_for('.shop'))

                        
            session['cart'].append(item)
            session.modified = True
            return redirect(url_for('.shop'))
        else:
            return "Item not found in stock"
    else:
        return 'Error while adding item to cart'


@app.route('/cart')
def cart():
    total_price = 0
    total_quantity = 0
    if 'cart' in session:
        for item in session['cart']:
            total_price += item['quantity'] * item['price']
            total_quantity += item['quantity']
        return render_template('cart.html', items=session['cart'], total_price=total_price, total_quantity=total_quantity)
    else:
        return render_template('cart.html')

@app.route('/empty')
def empty_cart():
    try:
        session.pop('cart', None)
        return redirect(url_for('.cart'))
    except Exception as e:
        print(e)

@app.route('/delete/<int:itemid>')
def delete_product(itemid):
    try:
        session.modified = True
        for i, item in enumerate(session['cart']):
            if item['itemid'] == itemid:
                session['cart'].pop(i)
                break
        return redirect(url_for('.cart'))
    except Exception as e:
        print(e)


@app.route('/update_quantity/<int:itemid>', methods=['POST'])
def update_quantity(itemid):
    try:
        quantity = int(request.form['quantity'])
        for i, item in enumerate(session['cart']):
            if item['itemid'] == itemid:
                session['cart'][i]['quantity'] = quantity
                session.modified = True
                break
        return redirect(url_for('.cart'))
    except Exception as e:
        print(e)


#----------------------------cart end------------------------------------------


    



@app.route('/checkout', methods =['GET', 'POST'])
def checkout():
    total_price = 0
    total_quantity = 0
    
    
    cursor = mysql.connection.cursor()
    mycursor.execute('SELECT  `name`, `address`, `phone`, `pin`, `state`, `district` FROM `userdetails` WHERE `username`=%s',(session['username'],))
    user=mycursor.fetchall()
    print(user)
   
    if 'cart' in session:
        for item in session['cart']:
            total_price += item['quantity'] * item['price']
            total_quantity += item['quantity']
            print(user)
        return render_template('checkout.html', items=session['cart'], total_price=total_price, total_quantity=total_quantity,user=user)
    else:
        return render_template("checkout.html") 
  

@app.route('/checkout')
def checkoutdisp():
    
    return render_template("checkout.html")   
 
@app.route('/about2')
def About():
    return render_template("about2.html")  
@app.route('/about3')
def About1():
    return render_template("about3.html")  

@app.route('/placeorder', methods=['POST'])
def placeorder():
    # Retrieve data from the session
    name = request.form['fname']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']
    state = request.form['state']
    district = request.form['district']
    zip = request.form['zip']
    
    cart = session.get('cart')
    orderid = secrets.token_urlsafe(4)
    mycursor.execute("INSERT INTO `shipping`(`name`, `email`, `phone`, `address`, `state`, `district`, `zip`, `ordid`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(name,email,phone,address,state,district,zip,orderid))
    # Insert cart data into the orders table
    for item in cart:
        mycursor.execute("INSERT INTO orders ( item_id, quantity, price, username, orderid) VALUES (%s, %s, %s, %s, %s)", ( item['itemid'], item['quantity'], item['price'], item['username'],orderid))
    # Commit the changes
    connection.commit()
    
    # Clear the cart from the session
    session.pop('cart', None)

    return render_template('cart.html')

@app.route('/orders', methods =['GET', 'POST'])
def orders():
    un=session['username']
    query = "SELECT `iname`,orders.quantity,orders.price,`order_date` FROM `orders` ,`stock` where `orders`.`item_id`=`stock`.`itemid` and `orders`.`status`='Accepted' and `username`='"+un+"'"
    mycursor.execute(query)
    orders=mycursor.fetchall()
    
    return render_template("/orders.html",orddata=orders)


# @app.route('/orders', methods =['GET', 'POST'])
# def orders():
#     total_price = 0
#     total_quantity = 0
#     mycursor.execute("SELECT * FROM userdetails WHERE id=%s", (session['user_id'],))
#     user_details = mycursor.fetchone()
#     if 'cart' in session:
#         for item in session['cart']:
#             total_price += item['quantity'] * item['price']
#             total_quantity += item['quantity']
#         return render_template('orders.html', items=session['cart'], total_price=total_price, total_quantity=total_quantity,user_details=user_details)
#     else:
#         return render_template("orders.html") 

@app.route('/orderdisp', methods =['GET', 'POST'])
def orderdisp():
    
    return render_template("orders.html")    
    
     

if __name__ =='__main__':
    app.run(debug="True")
     
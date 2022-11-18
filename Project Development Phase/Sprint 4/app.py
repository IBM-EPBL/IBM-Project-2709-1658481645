import os
import secrets
import isort
import autopep8
import black
from turtle import title
from unicodedata import category
from flask import Flask, render_template, request, redirect, url_for, session
from marshmallow import Schema, fields
import ibm_db
import bcrypt
import base64
import io
import mypy
 
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=fbd88901-ebdb-4a4f-a32e-9822b9fb237b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32731;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=lhk92942;PWD=Cht7cZes9VeaXQ5N",'','')

# url_for('static', filename='style.css')

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
 
@app.route("/")
def index():
  return render_template('index.html',name='Home')

@app.route("/order")
def order():
  return render_template('order.html',name='Home')

@app.route("/registerUser",methods=['GET'])
def register():
  if request.method == 'POST':
    username = request.form['username']
    email = request.form['email']
    phoneno = request.form['phoneno']
    password = request.form['password']

    if not username or not email or not phoneno or not password:
      return render_template('registerUser.html',error='Please fill all fields')
    hash=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    query = "SELECT * FROM user_detail WHERE email=? OR phoneno=?"
    stmt = ibm_db.prepare(conn, query)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.bind_param(stmt,2,phoneno)
    ibm_db.execute(stmt)
    isUser = ibm_db.fetch_assoc(stmt)
    if not isUser:
      insert_sql = "INSERT INTO user_detail(username, email, phoneno, password) VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, username)
      ibm_db.bind_param(prep_stmt, 2, email)
      ibm_db.bind_param(prep_stmt, 3, phoneno)
      ibm_db.bind_param(prep_stmt, 4, hash)
      ibm_db.execute(prep_stmt)
      return render_template('registerUser.html',success="You can login")
    else:
      return render_template('registerUser.html',error='Invalid Credentials')

  return render_template('registerUser.html',name='Home')

@app.route("/loginUser",methods=['GET','POST'])
def login():
    if request.method == 'POST':
      email = request.form['email']
      password = request.form['password']

      if not email or not password:
        return render_template('loginUser.html',error='Please fill all fields')
      query = "SELECT * FROM user_detail WHERE email=?"
      stmt = ibm_db.prepare(conn, query)
      ibm_db.bind_param(stmt,1,email)
      ibm_db.execute(stmt)
      isUser = ibm_db.fetch_assoc(stmt)
      print(isUser,password)

      if not isUser:
        return render_template('loginUser.html',error='Invalid Credentials')
      
      isPasswordMatch = bcrypt.checkpw(password.encode('utf-8'),isUser['PASSWORD'].encode('utf-8'))

      if not isPasswordMatch:
        return render_template('loginUser.html',error='Invalid Credentials')

      session['email'] = isUser['EMAIL']
      return redirect(url_for('home'))
    return render_template('loginUser.html',name='Home')

    


@app.route("/registerAdmin",methods=['GET','POST'])
def registerAd():
  if request.method == 'POST':
    adminname = request.form['adminname']
    email = request.form['email']
    phoneno = request.form['phoneno']
    password = request.form['password']

    if not adminname or not email or not phoneno or not password:
      return render_template('registerAdmin.html',error='Please fill all fields')
    hash=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    query = "SELECT * FROM admin_detail WHERE email=? OR phoneno=?"
    stmt = ibm_db.prepare(conn, query)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.bind_param(stmt,2,phoneno)
    ibm_db.execute(stmt)
    isUser = ibm_db.fetch_assoc(stmt)

    if not isUser:
      insert_sql = "INSERT INTO admin_detail(adminname, email, phoneno, password) VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, adminname)
      ibm_db.bind_param(prep_stmt, 2, email)
      ibm_db.bind_param(prep_stmt, 3, phoneno)
      ibm_db.bind_param(prep_stmt, 4, hash)
      ibm_db.execute(prep_stmt)
      return render_template('registerAdmin.html',success="You can login")
    else:
      return render_template('registerAdmin.html',error='Invalid Credentials')

  return render_template('registerAdmin.html',name='Home')

@app.route("/loginAdmin",methods=['GET','POST'])
def loginAd():
    if request.method == 'POST':
      email = request.form['email']
      password = request.form['password']

      if not email or not password:
        return render_template('loginAdmin.html',error='Please fill all fields')
      query = "SELECT * FROM admin_detail WHERE email=?"
      stmt = ibm_db.prepare(conn, query)
      ibm_db.bind_param(stmt,1,email)
      ibm_db.execute(stmt)
      isUser = ibm_db.fetch_assoc(stmt)
      print(isUser,password)

      if not isUser:
        return render_template('loginAdmin.html',error='Invalid Credentials')
      
      isPasswordMatch = bcrypt.checkpw(password.encode('utf-8'),isUser['PASSWORD'].encode('utf-8'))

      if not isPasswordMatch:
        return render_template('loginAdmin.html',error='Invalid Credentials')

      session['email'] = isUser['EMAIL']
      return redirect(url_for('addproduct'))

    return render_template('loginAdmin.html',name='Home')


@app.route("/addProduct", methods=['GET','POST'])
def addproduct():
  if request.method == 'POST':
    types=request.form['cc']
    name = request.form['name']
    image = request.form['image']
    categorie = request.form['categorie']
    rate = request.form['rate']

    if types =='shirt':
      insert_sql = "INSERT INTO SHIRT(name, image, categorie, rate) VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, image)
      ibm_db.bind_param(prep_stmt, 3, categorie)
      ibm_db.bind_param(prep_stmt, 4, rate)
      ibm_db.execute(prep_stmt)

    if types =='pant':
      insert_sql = "INSERT INTO PANT(name, image, categorie, rate) VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, image)
      ibm_db.bind_param(prep_stmt, 3, categorie)
      ibm_db.bind_param(prep_stmt, 4, rate)
      ibm_db.execute(prep_stmt)

    if types =='hat':
      insert_sql = "INSERT INTO HAT(name, image, categorie, rate) VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, image)
      ibm_db.bind_param(prep_stmt, 3, categorie)
      ibm_db.bind_param(prep_stmt, 4, rate)
      ibm_db.execute(prep_stmt)

    if types =='tops':
      insert_sql = "INSERT INTO TOPS(name, image, categorie, rate) VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, image)
      ibm_db.bind_param(prep_stmt, 3, categorie)
      ibm_db.bind_param(prep_stmt, 4, rate)
      ibm_db.execute(prep_stmt)

    if types =='saree':
      insert_sql = "INSERT INTO SAREE(name, image, categorie, rate) VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, image)
      ibm_db.bind_param(prep_stmt, 3, categorie)
      ibm_db.bind_param(prep_stmt, 4, rate)
      ibm_db.execute(prep_stmt)

    if types =='leggings':
      insert_sql = "INSERT INTO LEGGINGS(name, image, categorie, rate) VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, image)
      ibm_db.bind_param(prep_stmt, 3, categorie)
      ibm_db.bind_param(prep_stmt, 4, rate)
      ibm_db.execute(prep_stmt)

    if types =='tshirts':
      insert_sql = "INSERT INTO TSHIRTS (name, image, categorie, rate) VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, image)
      ibm_db.bind_param(prep_stmt, 3, categorie)
      ibm_db.bind_param(prep_stmt, 4, rate)
      ibm_db.execute(prep_stmt)

  return render_template('addproduct.html',success="You can login")


@app.route("/home",methods=['GET','POST'])
def home():
  shirt_list=[]
  pant_list=[]
  hat_list=[]
  saree_list=[]
  tshirt_list=[]
  tops_list=[]
  leggings_list=[]

  #selecting_shirt
  sql = "SELECT * FROM SHIRT"
  stmt = ibm_db.exec_immediate(conn, sql)
  shirt = ibm_db.fetch_both(stmt)
  while shirt != False :
      shirt_list.append(shirt)
      shirt = ibm_db.fetch_both(stmt)
  print(shirt_list)
  
 #selecting_pant
  
  sql1="SELECT * FROM PANT"
  stmt1 = ibm_db.exec_immediate(conn, sql1)
  pant=ibm_db.fetch_both(stmt1)
  while pant != False :
      pant_list.append(pant)
      pant = ibm_db.fetch_both(stmt1)
  print(pant_list) 

#selecting_hat
  sql2="SELECT * FROM HAT"
  stmt2 = ibm_db.exec_immediate(conn, sql2)
  hat=ibm_db.fetch_both(stmt2)
  while hat != False :
      hat_list.append(hat)
      hat = ibm_db.fetch_both(stmt2)
  print(hat_list)

  #selecting_saree
  sql3="SELECT * FROM SAREE"
  stmt3 = ibm_db.exec_immediate(conn, sql3)
  saree=ibm_db.fetch_both(stmt3)
  while saree != False :
      saree_list.append(saree)
      saree = ibm_db.fetch_both(stmt3)
  print(saree_list) 

  sql3="SELECT * FROM TSHIRTS"
  stmt3 = ibm_db.exec_immediate(conn, sql3)
  tshirt=ibm_db.fetch_both(stmt3)
  while tshirt != False :
      tshirt_list.append(tshirt)
      tshirt = ibm_db.fetch_both(stmt3)
  print(tshirt_list)

  sql3="SELECT * FROM TOPS"
  stmt3 = ibm_db.exec_immediate(conn, sql3)
  tops=ibm_db.fetch_both(stmt3)
  while tops != False :
      tops_list.append(tops)
      tops = ibm_db.fetch_both(stmt3)
  print(tops_list) 

  sql3="SELECT * FROM LEGGINGS"
  stmt3 = ibm_db.exec_immediate(conn, sql3)
  leggings=ibm_db.fetch_both(stmt3)
  while leggings != False :
      leggings_list.append(leggings)
      leggings = ibm_db.fetch_both(stmt3)
  print(leggings_list) 

  #returning to HTML
  return render_template('home.html',dictionary= shirt_list,pants=pant_list,hats=hat_list,sarees=saree_list,tshirts=tshirt_list,topss=tops_list,leggings=leggings_list)
  
@app.route("/data")
def display():
  shirt_list=[]
  pant_list=[]
  hat_list=[]
  saree_list=[]
  tshirt_list=[]
  tops_list=[]
  leggings_list=[]

  #selecting_shirt
  sql = "SELECT * FROM SHIRT"
  stmt = ibm_db.exec_immediate(conn, sql)
  shirt = ibm_db.fetch_both(stmt)
  while shirt != False :
      shirt_list.append(shirt)
      shirt = ibm_db.fetch_both(stmt)
  print(shirt_list)
  
 #selecting_pant
  
  sql1="SELECT * FROM PANT"
  stmt1 = ibm_db.exec_immediate(conn, sql1)
  pant=ibm_db.fetch_both(stmt1)
  while pant != False :
      pant_list.append(pant)
      pant = ibm_db.fetch_both(stmt1)
  print(pant_list) 

#selecting_watch
  sql2="SELECT * FROM HAT"
  stmt2 = ibm_db.exec_immediate(conn, sql2)
  hat=ibm_db.fetch_both(stmt2)
  while hat != False :
      hat_list.append(hat)
      hat = ibm_db.fetch_both(stmt2)
  print(hat_list)

  #selecting_rings
  sql3="SELECT * FROM SAREE"
  stmt3 = ibm_db.exec_immediate(conn, sql3)
  saree=ibm_db.fetch_both(stmt3)
  while saree != False :
      saree_list.append(saree)
      saree = ibm_db.fetch_both(stmt3)
  print(saree_list)  
  sql3="SELECT * FROM TSHIRTS"
  stmt3 = ibm_db.exec_immediate(conn, sql3)
  tshirt=ibm_db.fetch_both(stmt3)
  while tshirt != False :
      tshirt_list.append(tshirt)
      tshirt = ibm_db.fetch_both(stmt3)
  print(tshirt_list)
  sql3="SELECT * FROM TOPS"
  stmt3 = ibm_db.exec_immediate(conn, sql3)
  tops=ibm_db.fetch_both(stmt3)
  while tops != False :
      tops_list.append(tops)
      tops = ibm_db.fetch_both(stmt3)
  print(tops_list) 
  sql3="SELECT * FROM LEGGINGS"
  stmt3 = ibm_db.exec_immediate(conn, sql3)
  leggings=ibm_db.fetch_both(stmt3)
  while leggings != False :
      leggings_list.append(leggings)
      leggings = ibm_db.fetch_both(stmt3)
  print(leggings_list) 
  #returning to HTML
  return render_template('home.html',dictionary= shirt_list,pants=pant_list,hats=hat_list,sarees=saree_list,tshirts=tshirt_list,topss=tops_list,leggings=leggings_list)

@app.route("/orderplaced",methods=['GET','POST'])
def dis():
  if request.method == 'POST':
    pname=request.form['name']
    img=request.form['image']
    rate=request.form['rate']
    categorie=request.form['categorie']
  return render_template('order.html',pname=pname,img=img,rate=rate,categorie=categorie)
   
@app.route("/complete",methods=['GET','POST'])

def orderdisplay():
  if request.method == 'POST':
    name = request.form['order_name']
    image = request.form['order_image']
    rate = request.form['order_rate']
    categorie = request.form['order_categorie']
    insert_sql = "INSERT INTO DISPLAYORDER(name, image,rate, categorie) VALUES (?,?,?,?)"
    prep_stmt = ibm_db.prepare(conn, insert_sql)
    ibm_db.bind_param(prep_stmt, 1, name)
    ibm_db.bind_param(prep_stmt, 2, image)
    ibm_db.bind_param(prep_stmt, 3, rate)
    ibm_db.bind_param(prep_stmt, 4, categorie)
    ibm_db.execute(prep_stmt)      
  return render_template('success.html',success="You can login")

@app.route("/displayorder")
def displayorder():
  details_list=[]
  sql = "SELECT * FROM DISPLAYORDER"
  stmt = ibm_db.exec_immediate(conn, sql)
  detail = ibm_db.fetch_both(stmt)
  while detail != False :
      details_list.append(detail)
      detail = ibm_db.fetch_both(stmt)
  print(details_list)
  return render_template('displayorder.html',details=details_list)


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))
    
if __name__ == '__main__':
    port=int(os.environ.get('PORT',5000))
    app.run(port=port,host='0.0.0.0')
    app.debug=True

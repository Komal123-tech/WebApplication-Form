from flask import Flask,render_template,request
import pymysql

db=None
cur=None

def connectDb():
    global db,cur
    db=pymysql.connect(host="localhost",
                        user="root",
                        password="",
                        database="company_portal")
    cur=db.cursor()

def disconnectDb():
    cur.close()
    db.close()

def getAllEmployeeRecords():
    connectDb()
    selectquery="select * from vaccinations_records"
    cur.execute(selectquery)
    result=cur.fetchall()
    
    disconnectDb()
    return result 

def insertToEmployeeTable(name,email,address,city,office,age,number,vname,vstatus,vdate):
    connectDb()
    insertquery="insert into vaccinations_records(fullname,emailaddress,address,city,officelocation,age,mobilenumber,vaccinename,vaccinationstatus,dateofvaccination) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".\
        format(name,email,address,city,office,age,number,vname,vstatus,vdate)
    cur.execute(insertquery)
    db.commit()
    disconnectDb()

def deleteFromEmployeeTable(name):
    connectDb()
    deletequery="delete from vaccinations_records where fullname='{}'".format(name)
    cur.execute(deletequery)
    db.commit()
    disconnectDb()

def getOneEmployeeRecord(name):
    connectDb()
    selectquery="select * from vaccinations_records where fullname='{}'".format(name)
    cur.execute(selectquery)
    result=cur.fetchone()
    disconnectDb()
    return result 

def getOnlyOneEmployeeRecord(name):
    connectDb()
    selectquery="select * from vaccinations_records where fullname='{}'".format(name)
    cur.execute(selectquery)
    result=cur.fetchall()
    disconnectDb()
    return result 

def updateEmployeeTable(fullname,city,vaccinationstatus,officelocation,dateofvaccination):
    connectDb()
    updatequery='update vaccinations_records set city="{}", \
                officelocation="{}",vaccinationstatus="{}", dateofvaccination="{}" where fullname="{}"'.\
                    format(city,officelocation,vaccinationstatus,dateofvaccination,fullname)
    cur.execute(updatequery)
    db.commit()
    disconnectDb()

app=Flask(__name__)

@app.route('/')
def Home():
    return render_template('Home.html')


@app.route('/data')
def Employee():
    data=getAllEmployeeRecords()
    return render_template('Employee.html',data=data)

@app.route('/onlyread')
def ReadEmployee():
    data=getAllEmployeeRecords()
    return render_template('Employee_List.html',data=data)

@app.route('/View_details')
def ViewEmployeeRecords():
    data=getAllEmployeeRecords()
    return render_template('Display.html',data=data)

@app.route('/details/<name>')
def ViewoneEmployeeRecords(name):
    data=getOnlyOneEmployeeRecord(name)
    return render_template('Display.html',data=data)


@app.route('/form',methods=['GET','POST'])
def VaccinationForm():  
    if request.method=='POST':
        insertToEmployeeTable(request.form['fullname'],request.form['emailaddress'],request.form['address'],request.form['city'],
            request.form['officelocation'],request.form['age'],request.form['mobilenumber'],request.form['vaccinename'],request.form['vaccinationstatus'],request.form['dateofvaccination'])
        data=getAllEmployeeRecords()
        return render_template('Home.html',message='Details Submitted',data=data)
    else:
        return render_template('Vaccination Form.html')


@app.route('/update/<name>',methods=['GET','POST'])
def updateEmployee(name): 
    if request.method=='POST':
        updateEmployeeTable(name,request.form['city'],request.form['vaccinationstatus'],request.form['officelocation'],request.form['dateofvaccination'])
        data=getAllEmployeeRecords()
        return render_template('Employee.html',message='Update Completed',data=data)
    else:
        data=getOneEmployeeRecord(name)
        return render_template('update.html',data=data)



@app.route('/delete/<name>')
def deleteEmployee(name):
    deleteFromEmployeeTable(name)
    data=getAllEmployeeRecords()
    return render_template('Employee.html',message="Delete Completed",data=data)



@app.route('/adlogin',methods=['GET','POST'])
def result():
    mydb=pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="adminlogin"   
    )
    mycursor=mydb.cursor()
    if request.method=='POST':
        alogin=request.form
        Uname=alogin['username']
        Pword=alogin['password']
        mycursor.execute("Select * from admin_login where username='"+Uname+"' and password='"+Pword+"'")
        r=mycursor.fetchall()
        count=mycursor.rowcount
        if count==1:
            return render_template("Employee_List.html")
        else:
            return render_template("Loginform.html",message="Incorrect Username & Password")
    mydb.commit()
    mycursor.close()
    return render_template("Loginform.html")




   
if __name__=="__main__":
    app.run(debug=True)
    


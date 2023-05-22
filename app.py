from flask import Flask, request, render_template,jsonify
import joblib
import pandas as pd
import numpy as np
import pymysql

model = joblib.load('best_model_checkpoint.pkl')

app = Flask(__name__)

@app.route('/')
def welcome():
	return render_template('welcome.html')

@app.route('/rendersignup')
def rendersignup():
	return render_template('signup.html')

@app.route('/renderlogin')
def renderlogin():
	return render_template('login.html')


@app.route('/signup', methods=['POST'])
def signup():
    payload = request.json
    name = payload["name"]
    email = payload["email"]
    password = payload["password"]
    
    
    if email_exists(email):
        return jsonify({"result": "Email already exists"})
    
    if create_user(name, email, password):
        return jsonify({"result": "signup success"})
    
    return jsonify({"result": "signup failed"})


def email_exists(email):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='sudeep19',
        db='mysqldemo',
    )

    cur = conn.cursor()
    cur.execute("SELECT * FROM `users` WHERE `email` = %s", (email,))
    output = cur.fetchall()
    return len(output) > 0


def create_user(name, email, password):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='sudeep19',
        db='mysqldemo',
    )

    cur = conn.cursor()
    cur.execute("INSERT INTO `users` (`name`, `email`, `password`) VALUES (%s, %s, %s)", (name, email, password))
    conn.commit()
    
    return cur.rowcount > 0


@app.route('/login',methods=['POST'])
def login():
     
     paylod = request.json
     email = paylod["email"]
     password = paylod["password"]
     rawDAta = login1(email, password)
     if(len(rawDAta) == 0):
          return {"result" : "login unsuccess"}
     else:
          return {"result" : "login success"} 
    
  
  
def login1(email, password):
    conn = pymysql.connect(
        host='localhost',
        user='root', 
        password = "sudeep19",
        db='mysqldemo',
        )
      
    cur = conn.cursor()
    cur.execute("SELECT * FROM `users` WHERE `email` = %s AND `password` = %s", (email, password))
    output = cur.fetchall()
    return output


@app.route('/index')
def index():
	return render_template('index.html')
      

@app.route('/predict', methods=['GET','POST'])
def predict_disease():

    if request.method=='POST':
         
        payload = request.json
        AAP = payload['AAP']
        SGPT = payload['SGPT']
        TB = payload['TB']
        DB = payload['DB']
        SGOT = payload['SGOT']
        AGR = payload['AGR']
        ALBA = payload['ALBA']
        AGE=payload['AGE']
        GEN=payload['GEN']
        TP=payload['TP']


        input_arr = np.array([AGE,GEN,TB, DB, AAP, SGPT, SGOT,TP, ALBA, AGR], dtype=float)
        input_arr[1] = int(input_arr[1])
        result = model.predict([input_arr])[0]

        if(result==1):
            return "Patient has liver disease"
        if(result==0):
            return "Patient does not have liver disease"
    else:
        return render_template('index.html')

        
         

  



if __name__ == '__main__':
    app.run(debug=True)
 
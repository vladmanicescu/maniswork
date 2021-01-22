#!/bin/python3.7
import sqlite3
import flask
from flask import request, jsonify,render_template_string,render_template
import json
class my_database:
    def __init__(self,database_name):
        self.database_name = database_name
        self.my_connection = sqlite3.connect(self.database_name)
    def date_profesoare(self):
        self.my_cursor = self.my_connection.cursor()
        self.my_cursor.execute("SELECT * FROM Profesoare")
        self.result = self.my_cursor.fetchall()
        #print(self.result)
        #for i in self.result:
          #  print(i)
    def date_cursant_grupa_profesoara(self,query):
        self.my_cursor = self.my_connection.cursor()
        self.my_cursor.execute(query)
        self.result2 = self.my_cursor.fetchall()
        #print(self.result2)
    def _inserare_date_cursant_grupa_profesoara(self,query):
        self.my_cursor = self.my_connection.cursor()
        self.my_cursor.execute(query)
        self.my_connection.commit()

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html',length = 0, length2 = 0)

@app.route('/api/v1/resources/profesoare', methods=['GET'])
def get_teacher_info():
    db1 = my_database('cursanti.db')
    db1.date_profesoare()
    return jsonify(db1.result)

@app.route('/api/v1/resources/cursanti', methods=['GET'])
def get_teacher_student_info():
    query_parameters = request.args
    grupa = query_parameters.get('grupa')
    profesoara = query_parameters.get('profesoara')
    db1 = my_database('cursanti.db')
    query = f"select * from Cursanti where Grupa = '{grupa}' and Profesoara_asignata = '{profesoara}'"
    db1.date_cursant_grupa_profesoara(query)
    #return jsonify(db1.result2)
    return render_template('index.html', labels=db1.result2, length = len(db1.result2),length2 = 0 )
    #return '<h1>THis is a test<p>This is a test</p></h1>'

@app.route('/api/v1/resources/prezenta', methods=['GET'])
def get_presence():
    query_parameters = request.args
    grupa = query_parameters.get('grupa')
    profesoara = query_parameters.get('profesoara')
    db1 = my_database('cursanti.db')
    query = f"select * from Prezenta where Nume_Cursant in (select Nume from Cursanti where Grupa = '{grupa}' and Profesoara_asignata = '{profesoara}');"
    db1.date_cursant_grupa_profesoara(query)
    #return jsonify(db1.result2)
    return render_template('index.html', labels2=db1.result2, length2 = len(db1.result2),length = 0)

@app.route('/api/v1/resources/subiecte', methods=['GET'])
def get_subject():
    query_parameters = request.args
    grupa = query_parameters.get('grupa')
    profesoara = query_parameters.get('profesoara')
    lectia = query_parameters.get('lectia')
    db1 = my_database('cursanti.db')
    query = f"select * from subiect where Nume_Profesoara = '{profesoara}' and grupa = '{grupa}' and Nr_lectie = '{lectia}';"
    db1.date_cursant_grupa_profesoara(query)
    return jsonify(db1.result2)
@app.route('/api/v1/resources/aditie/cursanti', methods=['POST','GET'])
def add_cursant():
   #query_parameters = request.args
   #grupa = query_parameters.get('grupa')
   #profesoara = query_parameters.get('profesoara')
   #nume = query_parameters.get('nume')
   #prenume = query_parameters.get('prenume')
   #db1 = my_database('cursanti.db')
   #query = f"insert into cursanti values ('{prenume}','{nume}','{profesoara}','{grupa}');"
   #db1._inserare_date_cursant_grupa_profesoara(query)
   #result = request.form['grupa']
    #rint(result)
    detalii_cursant = [request.form[x] for x in ['grupa','profesoara','prenume','nume']]
    #print(detalii_cursant)
    db1 = my_database('cursanti.db')
    query = f"insert into cursanti values ('{detalii_cursant[-2]}','{detalii_cursant[-1]}','{detalii_cursant[0]}','{detalii_cursant[1]}');"
    db1._inserare_date_cursant_grupa_profesoara(query)
    #print(request.form[item])
    return render_template('index.html', length2 = 0, length = 0)

app.run(host='0.0.0.0')
#db1 = my_database('cursanti.db')
#db1.date_profesoare()

from flask import Flask, request, jsonify, send_file  
# jsonify => metodo para convertir un diccionario en un objeto json
from psycopg2 import connect, extras
# extras => método para que las consultas las devuelvan
# en forma de diccionarios en vez de tuplas
from cryptography.fernet import Fernet
# importo el metodo fernet para cifrar password.
from dotenv import load_dotenv
# importo dotenv para las variables de entorno
from os import environ
# para tener acceso a todas la variables de entorno

load_dotenv()
# cuando carge la app leerá el archivo .env

app = Flask(__name__)
# instancio app

key = Fernet.generate_key()
# instancio fernet que genera una clave para poder cifrar datos

host = environ.get("DB_HOST")
port = environ.get("DB_PORT")
dbname= environ.get("DB_NAME")
user = environ.get("DB_USER")
password = environ.get("DB_PASSWORD")
# environ => para obtener los valores de las variables de entorno 

# conexión básica a postgress
def get_connection():
   conn = connect(host=host, port=port, dbname=dbname, user=user, password=password)
   return conn

# http://localhost:5000/api/users
@app.get("/api/users")
def get_users():
   conn = get_connection()
   cur = conn.cursor(cursor_factory=extras.RealDictCursor)

   cur.execute("SELECT * FROM users")
   users = cur.fetchall()

   return jsonify(users)

# http://localhost:5000/api/users
@app.post("/api/users")
def create_user():
   conn = get_connection()
   cur = conn.cursor(cursor_factory=extras.RealDictCursor)
   # propiedad que devuelve un metodo que extrae los datos separados entre
   # parentesis "clave", valor. Formato diccionario

   new_user = request.get_json()
   # guardo la respuesta json() del objeto request
   username = new_user["username"]
   # guardo el valor que tiene username
   email = new_user["email"]
   # password = new_user["password"]
   password = Fernet(key).encrypt(bytes(new_user["password"], "utf-8"))
   # encrypta el password
   

   cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING *", 
               (username, email, password))
   # returning => retorna el dato insertado
   new_created_user = cur.fetchone()
   # extrae el dato del RETURNING *
   print (new_created_user)

   conn.commit()
   
   cur.close()
   conn.close()

   return jsonify(new_created_user)

# http://localhost:5000/api/users/id
@app.delete("/api/users/<id>")
def delete_user(id):
   conn = get_connection()
   cur = conn.cursor(cursor_factory=extras.RealDictCursor)

   cur.execute("DELETE FROM users WHERE id = %s RETURNING * ", (id, ))
   # ejecuta la consulta. RETURNING devuelve el dato que ha eliminado. 
   # (id, ) => es para indicar que es una tupla sino se pone la , da error
   user = cur.fetchone()
   # trae al usuario

   conn.commit()
   conn.close()
   cur.close()

   if user is None:
      return jsonify({ "message: usuario no existe" }), 404

   return jsonify(user)

@app.put("/api/users/<id>")
# ruta con parametro dinamico
def put_user(id):
# recibe el id como parametro
   conn = get_connection()
   cur = conn.cursor()

   user = request.get_json()
   username = user["username"]
   email = user["email"]
   password = Fernet(key).encrypt(bytes(user["password"], "utf-8"))

   cur.execute( "UPDATE users SET username = %s, email = %s, password = %s WHERE id = %s RETURNING *",
                  (username, email, password, id))
   update_user = cur.fetchone()
   print(update_user)

   conn.commit()
   cur.close()
   conn.close()

   if update_user is None:
      return jsonify({ "message: usuarion no encontrado" }), 404
   
   return jsonify(update_user)


@app.get("/api/users/<id>")
def get_user(id):
   conn = get_connection()
   cur = conn.cursor(cursor_factory=extras.RealDictCursor)

   cur.execute("SELECT * FROM users WHERE id = %s", (id,))
   # de todos los usuarios devuelve uno que coincida con el (id)
   user = cur.fetchone()

   conn.commit()
   conn.close()
   cur.close()

   if user is None:
      return jsonify({"message: usuario no existe"}), 404
      # si el usuario no existe devuelve un message y un 404

   return jsonify(user)

@app.get("/")
def home():
   return send_file("static/index.html")     

# si el nombre es igual al modulo principal main ejecuta run
if __name__ == "__main__":
   app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient, errors

app = Flask(__name__)

@app.route('/')
def index():
    error = request.args.get('error')
    return render_template('index.html', error=error)

@app.route('/select', methods=['POST'])
def select():
    user = request.form.get("user")
    passwd = request.form.get("passwd")
    database_name = request.form.get("database")

    try:
        conexion = MongoClient('192.168.1.146', 27017, username=user, password=passwd, authMechanism='SCRAM-SHA-256')
        db = conexion[database_name]
        collections = db.list_collection_names()

        return render_template('select_collection.html', collections=collections, user=user, passwd=passwd, database=database_name)
        
    except errors.PyMongoError:
        error = 'Error al conectar a la base de datos. Verifica tus credenciales.'
        return redirect(url_for('index', error=error))

@app.route('/show_collection', methods=['POST'])
def show_collection():
    user = request.form.get("user")
    passwd = request.form.get("passwd")
    database_name = request.form.get("database")
    collection_name = request.form.get("collection_name")

    try:
        conexion = MongoClient('192.168.1.146', 27017, username=user, password=passwd, authMechanism='SCRAM-SHA-256')
        db = conexion[database_name]
        collection = db[collection_name]
        documentos = list(collection.find())
        
        return render_template('show_collection.html', documentos=documentos, collection_name=collection_name)
    
    except errors.PyMongoError:
        error = 'No tienes permisos para ver esta colección.'
        return render_template('select_collection.html', error=error, collections=db.list_collection_names(), user=user, passwd=passwd, database=database_name)

if __name__ == '__main__':
    app.run(debug=True)

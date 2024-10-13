from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select', methods=['POST'])
def select():
    user = request.form.get("user")
    passwd = request.form.get("passwd")
    if user == "remoteuser":
        conexion = MongoClient(f'mongodb://{user}:{passwd}@192.168.1.146:27017/company')
    else:
        conexion = MongoClient('192.168.1.146', 27017, username=user, password=passwd)
    
    db = conexion.company
    
    # Obtener las colecciones
    collections = db.list_collection_names()
    return render_template('select_collection.html', collections=collections)

@app.route('/show_collection', methods=['POST'])
def show_collection():
    user = request.form.get("user")
    passwd = request.form.get("passwd")
    collection_name = request.form.get("collection_name")

    if user == "remoteuser":
        conexion = MongoClient(f'mongodb://{user}:{passwd}@192.168.1.146:27017/company')
    else:
        conexion = MongoClient('192.168.1.146', 27017, username=user, password=passwd)

    db = conexion.company
    collection = db[collection_name]
    documentos = list(collection.find())  # Convertir a lista para iterar en el template

    return render_template('show_collection.html', documentos=documentos, collection_name=collection_name)

if __name__ == '__main__':
    app.run(debug=True)

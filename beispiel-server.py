
"""
Example script showing how to represent todo lists and todo entries in Python
data structures and how to implement endpoint for a REST API with Flask.

Requirements:
* flask
"""

import uuid 

from flask import Flask, request, jsonify, abort


# initialize Flask server
app = Flask(__name__)

# create unique id for lists, entries
todo_list_1_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'
todo_list_2_id = '3062dc25-6b80-4315-bb1d-a7c86b014c65'
todo_list_3_id = '44b02e00-03bc-451d-8d01-0c67ea866fee'
todo_1_id = str(uuid.uuid4())
todo_2_id = str(uuid.uuid4())
todo_3_id = str(uuid.uuid4())
todo_4_id = str(uuid.uuid4())

# define internal data structures with example data
todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]
todos = [
    {'id': todo_1_id, 'name': 'Milch', 'description': '', 'list': todo_list_1_id},
    {'id': todo_2_id, 'name': 'Arbeitsblätter ausdrucken', 'description': '', 'list': todo_list_2_id},
    {'id': todo_3_id, 'name': 'Kinokarten kaufen', 'description': '', 'list': todo_list_3_id},
    {'id': todo_4_id, 'name': 'Eier', 'description': '', 'list': todo_list_1_id},
]

# add some headers to allow cross origin access to the API on this server, necessary for using preview in Swagger Editor!
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE, PATCH'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# Endpunkt um eine bestimmte TO-DO-Liste zu erhalten, zu löschen oder den Namen zu aktualisieren
@app.route('/todo-list/<list_id>', methods=['GET', 'DELETE', 'PATCH'])
def handle_list(list_id):
    # Suche TO-DO-Liste anhand der gegebenen ID
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    # Wenn die ID unvalide ist, wird der Status Code 404 zurückgeliefert
    if not list_item:
        abort(404)
    if request.method == 'GET':
        # Finde alle Einträge der gegebenen TO-DO-Liste (id)
        print('Returning todo list...')
        return jsonify([i for i in todos if i['list'] == list_id])
    elif request.method == 'DELETE':
        # Löscht die gegebene Liate
        print('Deleting todo list...')
        todo_lists.remove(list_item)
        return '', 200
    elif request.method == 'PATCH':
        # Aktualisiert den Namen der gegebenen Liste
        print('Patching todo list name...')
        list_item['name'] = request.get_json(force=True)
        return '', 200


# Endpunkt um eine neue Todo-Liste hinzuzufügen
@app.route('/todo-list', methods=['POST'])
def add_new_list():
    # Erstelle JSON von POST-Data
    new_list = request.get_json(force=True)
    print('Got new list to be added: {}'.format(new_list))
    # Erstelle neue UUID und weise der neuen Liste zu
    new_list['id'] = uuid.uuid4()
    todo_lists.append(new_list)
    return jsonify(new_list), 200


# Endpunkt um eine Liste aller Todo-Listen zurück zu liefern
@app.route('/todo-list', methods=['GET'])
def get_all_lists():
    return jsonify(todo_lists)

# Endpunkt um einen neues Eintrag in eine bestehende Liste hinzufügen
@app.route('/todo-list/<list_id>/entry', methods = ['POST'])
def new_entry_in_list(list_id):
    # Liste abrufen um auf existenz zu prüfen
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    # Wenn die ID unvalide ist, wird der Status Code 404 zurückgeliefert
    if not list_item:
        abort(404)
    
    # Daten aus POST-Data in JSON bringen und in Variablen einlesen
    name = request.get_json(force=True)['entry_name']
    description = request.get_json(force=True)['entry_description']
    new_todo = {'id': uuid.uuid4(), 'name': name, 'description': description, 'list': list_id}
    todos.append(new_todo)
    return '', 200

@app.route('/entry/<entry_id>', methods = ['PATCH', 'DELETE'])
def handle_entries(entry_id):
    entry = None
    if request.method == 'PATCH':
        print('Patching to do entry...')
        for todo in todos:
            if todo['id'] == entry_id:
                todo['name'] = request.get_json()['entry_name']
                todo['description'] = request.get_json()['entry_description']
                return '', 200
                         
        if not entry:
            abort(404)

    elif request.method == 'DELETE':
        print('Deleting to do entry')
        for todo in todos:
            if todo['id'] == entry_id:
                todos.remove(todo)
                return '', 200
                
            
        abort(404)



if __name__ == '__main__':
    # start Flask server
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

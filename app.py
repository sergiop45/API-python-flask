from flask import Flask, request, redirect, url_for, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'


db = SQLAlchemy(app)    
    

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())

with app.app_context():   
    db.create_all()

@app.route('/', methods=['GET'])
def home():
    nome = request.args.get("nome")
    return render_template("index.html")

@app.route('/users', methods=['GET'])
def all_users():
    try:
        users = User.query.all()
        users_dict = [user.__dict__ for user in users]
        for user in users_dict:
                user.pop('_sa_instance_state')  # remove a chave '_sa_instance_state' do dicionário

        return jsonify(users_dict)

    except Exception as error:
        return jsonify({"erro": error})

@app.route('/user', methods=["POST"])
def create_user():
   try:
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        print(name, email, password)

        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()


        return jsonify({
            'id': user.id,
            'name': user.name,
            'email': user.email
        })
   
   except Exception as error:
       return jsonify({"message": "erro!" }), 400


@app.route("/user/<id>", methods=["PUT", "GET"])
def edit_user(id):

    if request.method == "GET" :
        
        user = User.query.get(id)
        user_data = {'name': user.name, 'email': user.email}
        return jsonify(user_data)

    if request.method == "PUT" :
        try:
            user = db.session.get(User, id)
            user_edited = request.get_json() 

            user.name = user_edited["name"]
            user.email = user_edited["email"]
            user.password = user_edited["password"]

            db.session.commit()

            return jsonify({"message": "user edited!" }), 200

        
        except Exception as error:

            return jsonify({"message": "erro!" }), 400


@app.route('/user/<id>', methods=["DELETE"])
def delete_user(id):
    try:
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return render_template("index.html")
    
    except Exception as error:
        print("erro: ", error)
   

app.run(debug=True)


"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)



# Create a route to authenticate your users and return JWT Token
# The create_access_token() function is used to actually generate the JWT
@api.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not email or not password:
        return jsonify({"msg": "Email and Password are requiered"}), 400
    # Query your database for username and password
    user = User.query.filter_by(email=email, password=password).first()

    if user is None:
        # The user was not found on the database
        return jsonify({"msg": "Bad username or password"})
    
    if email != user.email and password != user.password:
        return jsonify({"msg": "Wrong email or password"}), 401

    
    # Create a new token with the user id inside
    access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=12))
    return jsonify({ "token": access_token, "user_id": user.id })

@api.route('/signup', methods=['POST'])
def signup():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not email or not password:
        return jsonify({"msg": "Missing requiered fields"}), 400
    
    user = User.query.filter_by(email=email).first()

    if user:
        return jsonify({"msg": "This user already exist"}), 409
    
    new_user = User(email=email, password=password, is_active=True)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token, "user":new_user.serialize()}), 201

@api.route('/update', methods=['PUT'])
@jwt_required()
def update_user():
    current_user = get_jwt_identity()

    user = User.query.filter_by(email= current_user.id).first()

    if user is None:
        return jsonify({"msg": "user not found"}), 404
    
    name = request.json.get("name", user.name)
    password = request.json.get("password", user.password)

    #ACTUALIZAMOS CAMPOS

    user.name = name
    user.password = password

    db.session.add(user)
    db.session.commit()

    return jsonify({'msg':"user updated"}), 200

@api.route('/private', methods=['GET'])
@jwt_required()
def private():

    #validate identity
    current_user = get_jwt_identity()

    user = User.query.get(current_user)

    return jsonify(user.serialize()), 200



@api.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    result = [user.serialize() for user in users]
    current_user_id = get_jwt_identity()
    print(current_user_id)
    return jsonify({'users' : result}), 200

@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

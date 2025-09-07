import os
import boto3
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt
from schemas import UserSchema

blp = Blueprint("Users", "users", description="Users Management")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('USERS_TABLE', 'users'))
blocklist_table = dynamodb.Table(os.environ.get('BLOCKLIST_TABLE', 'blocklist'))

def blacklist_token(jti, user_id):
    blocklist_table.put_item(Item={"id": f"TOKEN#{jti}", "user": user_id})

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        response = table.scan(FilterExpression="begins_with(id, :prefix) AND username = :username", ExpressionAttributeValues={":prefix": "USER#", ":username": user_data["username"]})
        items = response.get('Items', [])
        if items:
            abort(409, message="A user with that username already exists.")
        user_id = str(os.urandom(8).hex())
        hashed_password = pbkdf2_sha256.hash(user_data["password"])
        table.put_item(Item={"id": f"USER#{user_id}", "username": user_data["username"], "password": hashed_password})
        return {"message": "User created successfully."}, 201

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        response = table.scan(FilterExpression="begins_with(id, :prefix) AND username = :username", ExpressionAttributeValues={":prefix": "USER#", ":username": user_data["username"]})
        items = response.get('Items', [])
        user = items[0] if items else None
        if user and pbkdf2_sha256.verify(user_data["password"], user["password"]):
            access_token = create_access_token(identity=str(user["id"]), fresh=True)
            refresh_token = create_refresh_token(identity=str(user["id"]))
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        abort(401, message="Invalid credentials.")

@blp.route("/refresh")
class UserRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt()["jti"]
        blacklist_token(jti, current_user)
        return {"access_token": new_token}, 200

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        user_id = get_jwt_identity()
        blacklist_token(jti, user_id)
        return {"message": "Successfully logged out."}

    
@blp.route("/user/<string:user_id>")
class UserDetail(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        response = table.get_item(Key={"id": f"USER#{user_id}"})
        user = response.get("Item")
        if not user:
            abort(404, message="User not found.")
        return user

    def delete(self, user_id):
        response = table.get_item(Key={"id": f"USER#{user_id}"})
        user = response.get("Item")
        if not user:
            abort(404, message="User not found.")
            table.delete_item(Key={"id": f"USER#{user_id}"})
        return {"message": "User deleted."}, 200
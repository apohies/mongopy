from flask import Flask , request , jsonify ,Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util

# 

app = Flask(__name__)
#app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/mongoshu"
app.config["MONGO_URI"] = "mongodb+srv://apohies:b64EXr4RYm0pojls@cluster0.ykyig.mongodb.net/pymongo?retryWrites=true&w=majority"
mongo = PyMongo(app)




@app.route('/img/',methods=['GET'])
def cerre_siete():
   
    return "shato"

@app.route('/users',methods=['POST'])
def create_user():
    username =request.json['username']
    email=request.json['email']
    password = request.json['password']

    if username and email and password : 
        user = mongo.db.users.insert_one({'username':username , 'email':email , 'password': password})
        response = {'id' : str(user) ,'username' : username }

        return "creado"
    else :
        return not_found() 
   # 
    # online_users = mongo.db.products.find()

    return {'mensaje':'received'}

@app.route('/users',methods=['GET'])
def usuario():
    users=mongo.db.users.find()
    response=json_util.dumps(users)
    
    return Response(response,mimetype='application/json')

@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message':'Resource not found',
        'status':404
    })
    response.status_code = 404
    return response    

if __name__ == "__main__":
    app.run(debug=False)
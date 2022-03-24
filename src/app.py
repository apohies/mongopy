from flask import Flask , request , jsonify ,Response , redirect, url_for
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
import os
from werkzeug.utils import secure_filename
import cv2
import base64
import io
import PIL.Image as Image 
from byte_array import byte_data
import conection


UPLOAD_FOLDER = '.\src\space'
UPLOAD_FOLDER1 = '.\src\trace'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
#app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/mongoshu"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["MONGO_URI"] = conection.cast
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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/apostata', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            
            image = cv2.imread(f'.\src\space\{filename}')
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite('.\src\space\Test_gray.jpg', gray)
            return redirect(url_for('upload_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/check', methods=['GET'])
def check():
    image = open("src/space/onion.png",'rb')
    image_read = image.read()
    image_64_encode = base64.b64encode(image_read)
    b = base64.b64decode(image_64_encode)
    
    user = mongo.db.products.insert_one({'base64':image_64_encode})
    img = Image.open(io.BytesIO(b))
    img.save('castle.png')
    

   

    return "enconde"



if __name__ == "__main__":
    app.run(debug=False)
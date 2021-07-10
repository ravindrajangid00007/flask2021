from flask import Flask , jsonify , request , current_app ,Blueprint
# from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
import os
import time

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required


from ..models.student_model import db , Students
student_route = Blueprint('student_route', __name__ , url_prefix='/api/v1')




# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@student_route.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    student = Students.query.filter_by(email=email).first()
    if not student or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)


@student_route.route('/sign-up' , methods = ['POST'])
def createStudent():
    data = request.get_json()
    print(data)
    datatuple = Students(Firstname=data['name'] , Lastname=data['lastname'] , email=data['email'] , age=data['age'])
    db.session.add(datatuple)
    db.session.commit()
    return jsonify({'message': "creation successfully"}) ,200


@student_route.route('/students' , methods= ['GET'])
def getStudents():
    students = db.session.query(Students).all()

    results = []
    for student in students:
        dictu = {
            'Firstname': student.Firstname,
            'Lastname': student.Lastname,
            'age': student.age,
            'email': student.email,
            "avatar_path": student.avatar_path
        }
        results.append(dictu)
    return jsonify({'students': results})


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@student_route.route('/student/<int:id>', methods = ['GET'])
@jwt_required()
def GetStudent(id):
     # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    student = Students.query.filter_by(id=id).first()

    if current_user == student.email:
        results = {
            'Firstname': student.Firstname,
            'Lastname': student.Lastname,
            'age': student.age,
            'email': student.email
        }
        return jsonify({'student': results})
    return jsonify({ 'message': 'you are not authorized to see this profilie'}),401

def current_milli_time():
    return round(time.time() * 1000)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@student_route.route('/file/<int:id>' , methods=['PUT'])
@jwt_required
def put(self,id):
    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'message': 'no file part'})
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({'message': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.getcwd()  + current_app.config['UPLOAD_FOLDER']
        filename = str(current_milli_time())+filename
        file.save(os.path.join(path,filename))
        try:
            # s = students.update().where(students.columns.id == id).values({students.c.name == 'rakesk'})
            student = Students.query.filter_by(id=id).first()
            if student.avatar_path:
                os.remove(student.avatar_path)
            student.avatar_path = os.path.join(path,filename)
            db.session.commit()
            return jsonify({'message': 'fileuploaded'})
        except Exception as e:
            print(e)
from flask import Flask , jsonify , request
from flask_restful import Resource, Api


from werkzeug.utils import secure_filename
import os
import time

from kido_hobby.models.student import db , Students


api = Api()


UPLOAD_FOLDER = '/uploads/users/avatars'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}



def current_milli_time():
    return round(time.time() * 1000)

class CreateStudent(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        datatuple = Students(Firstname=data['name'] , Lastname=data['lastname'] , email=data['email'] , age=data['age'])
        db.session.add(datatuple)
        db.session.commit()
        return jsonify({'message': "creation successfully"})

class GetStudents(Resource):
    def get(self):
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

class GetStudent(Resource):
    def get(self , id):
        student = Students.query.filter_by(id=id).first()
        results = {
            'Firstname': student.Firstname,
            'Lastname': student.Lastname,
            'age': student.age,
            'email': student.email
        }
        return jsonify({'student': results})


class File(Resource):
    def allowed_file(filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def put(self,id):
        # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({'message': 'no file part'})
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return jsonify({'message': 'No selected file'})

        if file and File.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.getcwd()  + UPLOAD_FOLDER
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


# @app.route('/store/<string:name>/item')
# def get_items_in_store(name):
#     pass

api.add_resource(CreateStudent, '/create-student')
api.add_resource(GetStudents, '/students')
api.add_resource(GetStudent, '/student/<int:id>')
api.add_resource(File, '/file/<int:id>')
from flask import Flask,request,send_file
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db = SQLAlchemy(app)

class FileContent(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)

@app.route('/')
def index():
    return "INDEX"

@app.route('/upload',methods=["POST"])
def upload():
    file = request.files['inputFile']

    newFile = FileContent(name=file.filename,data=file.read())
    db.session.add(newFile)
    db.session.commit()
    return "saved " + file.filename + "to database"

@app.route('/download/<id>',methods=['GET'])
def download(id):

    filedata = FileContent.query.filter_by(id=id).first()
    return send_file(BytesIO(filedata.data),attachment_filename=filedata.name,as_attachment=True)

if __name__ == '__main__':
    app.run()

from flask import *
from flask_wtf import FlaskForm
from wtforms import FileField,SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from cryptography.fernet import Fernet
key= Fernet.generate_key()
with open("mykey.key",'wb') as mykey:
   mykey.write(key)
with open('mykey.key','rb') as mykey:
    key=mykey.read()
print(key)
f = Fernet(key)
with open('staticfiles/grades.csv','rb') as original_file:
    original=original_file.read()

encrypted=f.encrypt(original)
with open('enc_grades.csv','wb') as encrypted_file:
    encrypted_file.write(encrypted)
with open('enc_grades.csv', 'rb') as enc_file:
    enc = enc_file.read()
decrypted = f.decrypt(enc)
with open('dec_grades.csv', 'wb') as decrypted_file:
    decrypted_file.write(decrypted)
app = Flask(__name__)
app.config['SECRET_KEY']='supersecretkey'
app.config['UPLOAD_FOLDER']='staticfiles'

class UploadFileForm(FlaskForm):
    file=FileField("file",validators=[InputRequired()])
    submit=SubmitField("Upload File")

@app.route('/',methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])
def upload():
    form=UploadFileForm()
    if form.validate_on_submit():
        file=form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        return "File has been uploaded"
    return render_template("file_upload_form.html", form=form)

@app.route('/download')
def download_file():
    p="enc_grades.csv"
    return send_file(p, as_attachment=True)
@app.route('/download2')
def download_file2():
    p="dec_grades.csv"
    return send_file(p, as_attachment=True)
@app.route('/download3')
def download_file3():
    p="mykey.key"
    return send_file(p, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
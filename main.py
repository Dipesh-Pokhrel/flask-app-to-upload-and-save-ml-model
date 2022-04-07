from flask import Flask, redirect, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
import os

app = Flask(__name__)
db = SQLAlchemy(app)
Migrate(app,db)

UPLOAD_FOLDEDR = 'static/models'
ALLOWED_EXTENSIONS = set(['pkl','h5','sav','json','yaml'])
app.config['UPLOAD_FOLEDR'] = UPLOAD_FOLDEDR
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:database123@localhost/models'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super-secret-key'

# define database schema using class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(200), unique=True, nullable=False)
    model_type = db.Column(db.String(200), unique=True, nullable=False)
    engine_type = db.Column(db.String(100))
   #is_encrypted = db.Column(db.Boolean, default=False, nullable =False)

    def __init__(self,id,model_name,model_type,is_encrypted):
        self.id = id
        self.model_type = model_type
        self.model_name = model_name 
        self.is_encrypted = is_encrypted

    def __repr__(self) -> str:
        return f"{self.id}-{self.model_name}-{self.model_type}-{self.engine_type}"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
   return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_model():
	file = request.files['inputfile']
    
	if request.method == 'POST':	
		modelType = request.form['model_types']
		modelName = request.form['model_names']
		engineType = request.form['engine_types']
		return render_template('upload.html')
	filename = secure_filename(file.filename)

	if file in allowed_file(filename):
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		newFile = User(model_type=modelType,model_name=modelName,engine_type=engineType)
		db.session.add(newFile)
		db.session.commit()
		flash('Model successfuly uploaded' + file.filename + 'to the database!')
		return redirect('/')
	else:
		flash('Invalid upload. Upload only pkl,h5,sav,json,yaml')
		return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)

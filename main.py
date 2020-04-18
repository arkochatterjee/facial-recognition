from flask import Flask, request, render_template, redirect,url_for
from werkzeug import secure_filename
import pyrebase 
import datetime
from test import main
import os


#Add Config APIs




app = Flask(__name__,)


UPLOAD_FOLDER = 'static/image_upload/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])




@app.route('/',methods=['POST','GET'])   
def index1():
    if request.method == 'POST':
    # check if the post request has the file part
        '''
        if 'file' not in request.files:
            print("NO")
            return render_template('index.html', submit = False)
            '''
       
       
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print("NEI")
            return render_template('index.html', submit = False)

        if file and allowed_file(file.filename):
            print("OK")
            
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

            fullpath = UPLOAD_FOLDER+filename
            print(fullpath)

            ans = main(fullpath)

            return render_template('index.html', submit = True, result = ans)
            





            
            
    return render_template('index.html', submit = False)




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS    

app.secret_key = "coronadwd-srm"


if __name__ =='__main__':  
    app.run(host='0.0.0.0',debug=True, port=8080) 
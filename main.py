import os
from werkzeug.utils import secure_filename
from flask import Flask,render_template,jsonify,request
from mymaputils import allowed_file,getmapdata,getmapdatacsv
mmap_api_key = 'AIzaSyCh2wjSyEXOrTlrXtiGatvlaOKga6Umvwc'
app = Flask(__name__)


#Home ROUTE#
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

#UPLOAD FILE ROUTE#
@app.route('/upload', methods=['POST'])
def file_converter():
    if request.method == "POST":
        try:
            files = request.files.getlist('file')
            #print("files", files)
            if len(files) > 0:
                for data in files:
                    if allowed_file(data.filename):
                        filename = secure_filename(data.filename)
                        extension = filename.split('.')
                        file_path = os.path.join('static/uploads', filename)
                        data.save(file_path)
                        if extension[-1] == "csv":
                            if getmapdatacsv(file_path):
                                return "<a href='"+file_path+"' style='display:inline-block;margin-top:50px;background-color: #c058fc;border: none;color: white;padding: 15px 32px;text-align: center;text-decoration: none;text-transform:uppercase;font-weight:bold;font-size: 20px;margin: 4px 2px;cursor: pointer;'>Download The File</a>"
                            else:
                                return jsonify({"status": "failes", "message": "WORK FAILED !!!"})
                        elif getmapdata(file_path,filename):
                            return "<a href='"+file_path+".csv' style='display:inline-block;margin-top:50px;background-color: #c058fc;border: none;color: white;padding: 15px 32px;text-align: center;text-decoration: none;text-transform:uppercase;font-weight:bold;font-size: 20px;margin: 4px 2px;cursor: pointer;'>Download The File</a>"
                        else:
                            return jsonify({"status": "failes", "message": "WORK FAILED !!!"})
                    
                    else:
                        return jsonify({"status": "failed", "message": "File Format Not Allowed !! only 'xlsx','xlsm','xltx','xltm','csv' formats are allowed"})
            else:
                return jsonify({"status": "Please Upload a File"})
        except Exception as e:
            print("Exception Occurred", e)
            return jsonify({"status": "exception", "message": "Something Went Wrong post!!"})
    else:
        return jsonify({"status": "failed", "message": "Method Not Allowed !"})

#remove all files ROUTE#
@app.route('/remove', methods=['GET'])
def remove():
    for f in os.listdir('static/uploads'):
        try:
            os.remove(os.path.join('static/uploads', f))
        except:
            return jsonify({"status": "failed", "message": "something Went wrong"})
    return jsonify({"status": "success", "message": "All Files Removed Successfully !"})

# run the project
if __name__ == '__main__':
    app.run(port=9000,debug=True)
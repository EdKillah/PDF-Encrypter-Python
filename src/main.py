from flask import Flask, render_template, request, redirect, send_from_directory, abort
import os
from werkzeug.utils import secure_filename
from encrypter import secure_pdf

app = Flask(__name__)

app.config["PDF_UPLOADS"] = os.path.join(app.static_folder, 'pdfs','uploads')
app.config["VALID_EXTENSIONS"] = "PDF"
app.config["VALID_MAXIMUM_SIZE"] = 5200000                                   


def allowed_size(file_size):
    is_valid = False
    #this is just to work the deploy
    if int(file_size) <= app.config["VALID_MAXIMUM_SIZE"]:
        is_valid = True

    return is_valid

def allowed_extension(file):
    
    is_valid = False
    if("." in file):
        file = file.rsplit('.',1)[1]
        print("file: ",file)

        if file.upper() == app.config["VALID_EXTENSIONS"]:
            is_valid = True
    
    return is_valid


def encrypt(filename, password):
    secure_pdf(app.config["PDF_UPLOADS"],filename, password)
    print("A punto de descargar el pdf cifrado...")
    try:
        print("ENTRO EN TRY!")
        return send_from_directory(app.config["PDF_UPLOADS"], filename=f"encrypted_{filename}", as_attachment=True)
    except FileNotFoundError: 
        print("No funciono la descarga!")
        abort(404)



@app.route('/', methods=['GET','POST'])
def upload_image():

    if request.method == "POST":

        if request.files: 

            pdf = request.files["pdf"]

            print("LA CONTRASEÑA: ",request.form["password"])

            if pdf.filename == '':
                print("The pdf must to have a valid name.")

            elif not allowed_extension(pdf.filename):
                print("The extension is not allowed.")

            elif not allowed_size(request.cookies.get("filesize")):
                print("The size is too big, try with another smaller.")
                #here we can handle errors
            
            else:
                #we save the pdf with a method from the filestorage object
                filename = secure_filename(pdf.filename)
                print("NUEVO FILENAME: ",filename)
                pdf.save(os.path.join(app.config["PDF_UPLOADS"], filename))
                print("pdf saved!")
                return encrypt(filename, request.form["password"])
                
            

        return redirect(request.url)


    return render_template('encrypt_pdf.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)
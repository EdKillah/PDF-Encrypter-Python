from PyPDF2 import PdfFileWriter, PdfFileReader
import os

def secure_pdf(file, name, password):

    print("Va a comenzar a cifrar")
    print("FILE A CIFRAR: ",file)
    print("NOMBRE CON EL QUE VA A QUEDAR: ",name)
    print("PASSWORD PARA CIFRAR: ",password)
    parser = PdfFileWriter()
    pdf = PdfFileReader(os.path.join(file,name))
    print("comenzando a recorrer las paginas")
    for page in range(pdf.numPages):
        parser.addPage(pdf.getPage(page))
    parser.encrypt(password)
    print("Creando nuevo archivo cifrado")
    with open(os.path.join(file,f"encrypted_{name}"), "wb") as f:
        parser.write(f)
        f.close()
    print("Creo el archivo correctamente")
    print(f"encrpyted_{name} Created...")


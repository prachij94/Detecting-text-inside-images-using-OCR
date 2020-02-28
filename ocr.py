"""
This script initially checks using the Pytesseract library if there is any text at all in an image.
If some text is found, only then the script call to the Cloud Vision API is made using a call to the Powershell script.
"""
#OCR Using Image URL


#Reading required libraries
import pytesseract
from PIL import Image
from PIL import ImageFilter
import requests
from io import BytesIO
import numpy as np
import pandas as pd
import subprocess

#Pytesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'


#Function call for hitting the Cloud Vision API using a powershell script
def callpowershell(url):
    
     # The path of the powershell executable and also the path of the powershell script
     powerShellPath = r'C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe'
     powerShellCmd = "C:\\Users\\prachi\\Desktop\\OCR\\ocr.ps1"    #the powershell script takes as an argument the input image url
     
     
     #calling the powershell script
     p = subprocess.Popen([powerShellPath, '-ExecutionPolicy', 'Unrestricted', powerShellCmd, url],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
     output, error = p.communicate()
     
     #The extracted text is outputted along with the input image url
     if(p.returncode==0):
         print("\nExtracted Text:\n\n" + str(output))
         imagewithtext.set_value(row,'imageurl',url)
         imagewithtext.set_value(row,'Extracted Text',str(output))
 

#the input list of image urls
imageurlslist=np.loadtxt("C:\\Users\\prachi\\Desktop\\OCR\\ocrurlsforbannedimages.txt",dtype="str").tolist()

#Changing smaller dimension images to higher size i.e. 500x500
imageurlslist=[s.replace("250x250.jpg","500x500.jpg") for s in imageurlslist]
imageurlslist=[s.replace("250x250.jpeg","500x500.jpeg") for s in imageurlslist]
imageurlslist=[s.replace("250x250.png","500x500.png") for s in imageurlslist]


#Creating an output dataframe
imagewithtext = pd.DataFrame(columns=['imageurl','Extracted Text'])
row=0


#Iterating over the urls one at a time
for j in imageurlslist:
    
    #Reading the image from its url
    response = requests.get(j)
    if(response.status_code==404 or response.status_code==400):
        continue
    if(response.status_code!=200):
        response = requests.get(j.replace("500x500.","250x250."))
        
    #Extracting text using Python's library Pytesseract
    img = pytesseract.image_to_string(((Image.open(BytesIO(response.content))).convert('RGB')).filter(ImageFilter.SHARPEN))
    
    
    
    #If there is some text longer than 2 characters extracted, then we proceed to calling the powershell script for hitting the Cloud Vision API
    if((img!= "") and (len(img)>2)):
        print("*********Cloud Vision API will be called as text is present in image "+j+"  *************")
        
        callpowershell(j)
        row+=1
        print("\n")
    
    else:
        print("*************No text present in "+j+" *************")
        
imagewithtext.to_csv('BannedImagesWithExtractedText.csv',index=False)

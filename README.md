# Detecting-text-inside-images-using-OCR

The [Google Cloud Vision API](https://cloud.google.com/vision) is very effective for reading any text that may be present inside an image. It is suitable for more than [50 languages](https://cloud.google.com/vision/docs/languages) and various [file types](https://cloud.google.com/vision/docs/supported-files).It uses machine learning to help us understand our images with industry-leading prediction accuracy.


## Prerequisites:
A google cloud account should be already created and billing enabled for the Vision API project. The API environment should be set in the local system terminal/cmd using the [setup](https://cloud.google.com/vision/docs/setup) steps given in the documentation. 

This ensures that the powershell script(.ps1) file in this repository will be able to grab the the authorization credentials from the system environment.

## The procedure:

An input text file containing the url's of the images to be tested is read in the python script. Each url is first tested with python's OCR library **pytesseract** for an initial check on presence of any text at all or presence if more than 2 characters in the image. This is done to avoid any unnecessary hits directly to the Google Cloud Vision API. Please refer its [pricing policy](https://cloud.google.com/vision/pricing) for details.

If there are more than 2 characters present in the input image url, a call is made to the powershell file using python's *subprocess()*. Th powershell file authenticates the user using his already saved credentials in the environment. After this, it invokes the Vision APi with the input url and returns the text results to the python script.

The python script then saves the input url and extracted text into a dataframe and this process goes on iteratively for each url in the input text file.

The dataframe with all the extracted text details is finally saved as a csv file for further analysis on the text content.

# Requirements
- pytesseract
- PIL (pillow)
- requests
- subprocess
- io
- numpy
- pandas


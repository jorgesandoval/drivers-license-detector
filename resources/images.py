import os
import cv2
import imutils
from app import app
from skimage.metrics import structural_similarity
from PIL import Image
from flask_restful import Resource
from flask import request, render_template

class Image(Resource):

    def resizeImage(self, file):
        return Image.open(file).resize((250,160))

    def transformGrayScale(self, file):
        return cv2.cvtColor(file, cv2.COLOR_BGR2GRAY)

    def calculateStructuralSimilarity(self, file1, file2):
        (score, diff) = structural_similarity(file1, file2, full=True)
        diff =  (diff * 255).astype("uint8")
        return score, diff

    def transformThreshold(self, diff):
        return cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    def findCountours(self, thresh):
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        return cnts
    
    def drawCountours(self, file, cnts):
         for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(file, (x, y), (x + w, y + h), (0, 0, 255), 2)
              
    def post(self, score):
        return render_template('index.html',pred=str(round(score*100,2)) + '%' + ' correct')

    
    def get(self):
        return render_template("index.html")
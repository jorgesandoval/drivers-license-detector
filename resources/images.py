import cv2
import os
from app import app
from skimage.metrics import structural_similarity
from PIL import Image
from flask_restful import Resource 

class ImageModification(Resource):
    def resizeImage(self, file):
        return Image.open(file).resize(250,160)

    def transformGrayScale(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def calculateStructuralSimilarityDiff(self, file1, file2):
        (score, diff) = structural_similarity(file1, file2, full=True)
        diff =  (diff * 255).astype("uint8")
        return diff

    def calculateStructuralSimilarityScore(self, file1, file2):
        (score, diff) = structural_similarity(file1, file2, full=True)
        return score

    def transformThreshold(self, diff):
        return cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

class Image(Resource):

    def __init__(self, upload, original):
        self.upload = 'model/uploads'
        self.original = 'model/original'

    def post(self, file):
        originalImage = ImageModification.transformGrayScale(ImageModification.resizeImage(os.path.join(self.original,'driverslicencefront.png')))
        uploadImage = ImageModification.transformGrayScale(ImageModification.resizeImage(os.path.join(self.upload,file)))
        score = ImageModification.calculateStructuralSimilarityScore(self, originalImage, uploadImage)
        return {'score': str(round(score*100,2)) + '%' + ' correct'}
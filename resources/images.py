import cv2
import os
from skimage.metrics import structural_similarity
from flask_restful import Resource 

class ImageModification(Resource):
    def resizeImage(self, file):
        #img = cv2.imread(file, cv2.IMREAD_UNCHANGED)
        return cv2.resize(cv2.imread(file, cv2.IMREAD_UNCHANGED), (250,150), interpolation = cv2.INTER_AREA)

    def transformGrayScale(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def calculateStructuralSimilarityDiff(self, img1, img2):
        (score, diff) = structural_similarity(img1, img2, full=True)
        diff =  (diff * 255).astype("uint8")
        return diff

    def calculateStructuralSimilarityScore(self, file1, file2):
        (score, diff) = structural_similarity(file1, file2, full=True)
        return score

class ImageREST(Resource):

    def post(self, file):
        upload = './models/upload/' 
        original = './models/original/'
        try:
            originalImage = ImageModification.transformGrayScale(self,ImageModification.resizeImage(self, os.path.join(original,'DriversLicenseFront.png')))
            uploadImage = ImageModification.transformGrayScale(self,ImageModification.resizeImage(self, os.path.join(upload, file)))
            score = ImageModification.calculateStructuralSimilarityScore(self, originalImage, uploadImage)
            return {'score': str(round(score*100,2)) + '%' + ' correct'}, 200
        except:
            return {'message': 'An error was found processing your image - {}'.format(os.path.join(upload,file))}, 500



class Image(Resource):

    def post(self, ):
        return render_template('index.html',pred=str(round(score*100,2)) + '%' + ' correct')

    def get(self):
        return render_template("index.html")
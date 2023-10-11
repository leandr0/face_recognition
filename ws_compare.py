# This is a _very simple_ example of a web service that recognizes faces in uploaded images.
# Upload an image file and it will check if the image contains a picture of Barack Obama.
# The result is returned as json. For example:
#
# $ curl -XPOST -F "file=@004.jpeg" http://127.0.0.1:5001
#
# Returns:
#
# {
#  "face_found_in_image": true,
#  "is_picture_of_obama": true
# }
#
# This example is based on the Flask file upload example: http://flask.pocoo.org/docs/0.12/patterns/fileuploads/

# NOTE: This example requires flask to be installed! You can install it with pip:
# $ pip3 install flask

import face_recognition
from flask import Flask, jsonify, request, redirect

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            return detect_faces_in_image(file)

    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <title>Is this a picture of Obama?</title>
    <h1>Upload a picture and see if it's a picture of Obama!</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''


def detect_faces_in_image(file_stream):
    # Pre-calculated face encoding of Obama generated with face_recognition.face_encodings(img)
    known_face_encoding = [-9.75701809e-02,  4.50523421e-02,  3.50640304e-02, -6.43265322e-02,
             -1.75085664e-03, -5.13304844e-02,  2.41190288e-02, -9.26836133e-02,
              1.39520109e-01, -5.36627956e-02,  1.94615975e-01, -1.42055638e-02,
             -2.39148393e-01, -1.65335253e-01,  6.89404756e-02,  1.78628147e-01,
             -9.72628742e-02, -1.18553437e-01, -1.19559646e-01, -1.33137226e-01,
             -3.42566520e-04,  2.97404453e-03, -3.14479321e-03,  2.99230143e-02,
             -1.91479713e-01, -3.44923139e-01, -1.05110697e-01, -2.62783021e-02,
             -2.57869717e-02, -5.83150089e-02,  3.74814942e-02,  7.03320950e-02,
             -1.21913195e-01, -6.61994889e-02,  7.69810975e-02,  1.41414255e-01,
             -3.27518284e-02, -8.93676430e-02,  2.13366300e-01,  7.39527568e-02,
             -1.13571383e-01, -4.46570218e-02,  8.57399255e-02,  3.50746661e-01,
              1.88843220e-01,  5.80260716e-03,  1.02208048e-01, -4.39307094e-03,
              2.02694952e-01, -2.11484998e-01,  4.95571233e-02,  5.84688894e-02,
              9.18124169e-02,  3.17272469e-02,  1.59146324e-01, -1.48457915e-01,
              3.19630504e-02,  2.36449048e-01, -2.29016930e-01,  5.16295210e-02,
              1.55821741e-02, -1.09004594e-01, -9.42132100e-02, -8.40257555e-02,
              1.95632935e-01,  5.06016985e-02, -1.78310692e-01, -8.49931166e-02,
              1.64288312e-01, -6.81928992e-02,  1.10620297e-02,  2.20797136e-02,
             -1.68010563e-01, -1.67312711e-01, -3.91921848e-01,  8.49368572e-02,
              4.10066158e-01,  1.03911743e-01, -1.70944929e-01, -2.38241404e-02,
              4.39850390e-02, -9.89910960e-03,  8.13034102e-02,  1.09016158e-01,
             -7.77715445e-02, -1.09162331e-02, -9.47578698e-02,  4.75933850e-02,
              1.60472348e-01,  6.77725822e-02, -5.22279032e-02,  1.58767939e-01,
             -3.10296100e-02,  9.56584513e-03, -2.78397352e-02,  4.26674485e-02,
             -1.67471617e-01, -5.84427454e-03, -9.87648442e-02, -1.72874257e-02,
              8.47643986e-02, -1.07451707e-01,  5.26744872e-02,  1.27203107e-01,
             -1.86746299e-01,  1.93158329e-01,  7.75565207e-03,  1.54947750e-02,
             -5.73187023e-02, -3.00058573e-02, -1.13815069e-01,  4.20117080e-02,
              1.20654292e-01, -2.57748246e-01,  7.90993199e-02,  2.15095967e-01,
              5.62388822e-03,  1.17697909e-01,  4.12035994e-02,  6.96589053e-03,
             -1.75990686e-02,  3.41475010e-02, -1.84232533e-01, -5.08169681e-02,
              8.12850893e-04, -3.68634015e-02,  1.07272148e-01,  2.92337835e-02]
    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image
    unknown_face_encodings = face_recognition.face_encodings(img)

    face_found = False
    is_obama = False

    if len(unknown_face_encodings) > 0:
        face_found = True
        # See if the first face in the uploaded image matches the known face of Obama
        match_results = face_recognition.compare_faces([known_face_encoding], unknown_face_encodings[0])
        if match_results[0]:
            is_obama = True

    # Return the result as json
    result = {
        "face_found_in_image": face_found,
        "is_picture_of_obama": is_obama
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
import cv2
import joblib
import numpy as np
from skimage.feature import hog
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


TRUTH = {0: 'Forged', 1: 'Genuine'}

# Step 2: Extract HOG features from signatures
def extract_hog_features(images):
    hog_features = []
    img_list = []
    for image in images:
        fd, img = hog(image, orientations=5, pixels_per_cell=(6, 6), block_norm='L1-sqrt', cells_per_block=(1, 1), visualize=True)
        hog_features.append(fd)
        img_list.append(img)
    return hog_features, img_list


# Assuming you have a function to get a list of registered users
def get_users(user=None, user_flag=None):
    user_dict = {'049': ['049/01_049_gen.png', '049/01_0114049_fake.PNG', '049/01_0206049_fake.PNG', '049/01_0210049_fake.PNG', '049/02_049_gen.png', '049/02_0114049_fake.PNG', '049/02_0206049_fake.PNG', '049/03_049_gen.png', '049/04_049_gen.png'],
                 '050': ['050/01_050_gen.png', '050/01_0125050_fake.PNG', '050/01_0126050_fake.PNG', '050/01_0204050_fake.PNG', '050/02_050_gen.png', '050/02_0125050_fake.PNG', '050/03_050_gen.png', '050/04_050_gen.png', '050/04_0204050_fake.PNG', '050/05_050_gen.png'],
                 '060': ['060/H-S-160-F-04.png', '060/H-S-160-F-05.png', '060/H-S-160-F-28.png', '060/H-S-160-F-29.png', '060/H-S-160-F-30.png', '060/H-S-160-G-01.png', '060/H-S-160-G-02.png', '060/H-S-160-G-03.png', '060/H-S-160-G-04.png'],
                 '070': ['070/H-S-159-F-09.png', '070/H-S-159-F-10.png', '070/H-S-159-F-11.png', '070/H-S-159-F-12.png', '070/H-S-159-F-13.png', '070/H-S-159-G-02.png', '070/H-S-159-G-03.png', '070/H-S-159-G-04.png', '070/H-S-159-G-05.png', '070/H-S-159-G-06.png'],
                }
    if user_flag:
        return list(user_dict.keys())
    else:
        print('user__________', user)
        if user in ['060', '070']:
            user_file = user_dict[user][-1]
        else:
            user_file = user_dict[user][0]
        return user_dict[user], user_file


def validate_signature(signature_path):
    print(signature_path)
    img = cv2.imread(signature_path, cv2.IMREAD_GRAYSCALE)
    print("______________", img.shape)
    img = cv2.resize(img, (128, 64))
    hog_feature = extract_hog_features([img])
    if 'H-S-' in signature_path:
        svm_classifier = joblib.load('static\models\svm_classifier_model_hindi_final.pkl')
    else:
        svm_classifier = joblib.load('static\models\svm_classifier_model.pkl')
    y_pred = svm_classifier.predict(hog_feature[0])
    predicted_class = y_pred[0]
    return TRUTH[predicted_class]


@app.route('/')
def index():
    users = get_users(user_flag=True)
    return render_template('index.html', users=users)

# Route to return image list of user and one random genuine image of the user
@app.route('/user_signatures', methods=['POST'])
def load_signatures():
    user_name = request.form['user_name']
    signatures, genuine_signature = get_users(user_name)

    return jsonify({'signatures': signatures, 'genuine_signature': genuine_signature})


@app.route('/validate_signature', methods=['POST'])
def validate_signature_route():
    selected_signature = request.form['selected_signature']
    image_data = request.form['image_data']

    print(image_data)
    print(selected_signature)
    # Validate the saved image
    validation_result = validate_signature(image_data[1:])

    return jsonify({'result': validation_result})


if __name__ == '__main__':
    app.run(debug=True)

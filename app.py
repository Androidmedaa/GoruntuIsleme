from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from flask_cors import CORS 
import tensorflow as tf

from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import io
import base64

app = Flask(__name__)
CORS(app)

model = tf.keras.models.load_model('my_model.keras')

def predict_shape(img_data):

    img_data = img_data.split(',')[1]
    img_data = base64.b64decode(img_data)
    img = Image.open(io.BytesIO(img_data)).convert('RGB')

    img = img.resize((224, 224))

    img_array = np.array(img) / 255.0

    img_array = np.expand_dims(img_array, axis=0)

    # Tahmin yap
    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction, axis=1)[0]

    # Şekil sınıfına göre isim döndürme
    shapes = ['Daire','Uçurtma','Paralel','Dikdörtgen','Eşkenar dörtgen','Kare', 'Yamuk', 'Üçgen']  
    return shapes[predicted_class]


@app.route('/detect', methods=['POST'])
def detect_shape():
    data = request.get_json()
    img_data = data['image']

    # Tahmin yap
    shape = predict_shape(img_data)

    # Sonucu döndür
    return jsonify({'shape': shape})

if __name__ == '__main__':
    app.run(debug=True)

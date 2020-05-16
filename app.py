import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)
    if output>= 0.70:
        return render_template('index.html', prediction_text='Affecting with heart disease rate is : {}  high contact doctor immediately'.format(output))
    elif output<=0.40:
        return render_template('index.html', prediction_text='Affecting with heart disease rate is : {} is low , take care of your health'.format(output))
    else:
        return render_template('index.html', prediction_text='Affecting with heart disease rate is : {} contact doctor with in 3 days'.format(output))

    return render_template('index.html', prediction_text='Affecting with heart disease rate : {}'.format(output))
    if output>= 0.70:
        return ("contact doctor immeadiately")

@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)

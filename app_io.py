import os
import json
import requests
from flask import Flask, request, render_template, redirect

# Mute requests insecure warnings 
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


app = Flask(__name__)

model = 'Elda_DistilBert_5Langs'
url ="https://research-workspace.a3.saagie.io/app/f0f4fc39-14ac-4215-b02a-4cfe87dac8e5"#os.environ["APP_URL"]

def predict_text(data, model_name, serve_url=url, data_type='json'):
    """Inference with POST requests """
    if data_type == 'json':
        headers = {'Content-Type': 'application/json'}
    pred_url = serve_url + '/8080/predictions/' + model_name
    if type(data) == str: # if batch size = 1
        data = [data,] 
    data = json.dumps(data)
    response = requests.post(pred_url, headers=headers, data=data, verify=False)
    return response._content.decode('utf-8')


@app.route("/",methods=['GET','POST'])
def login():
    if request.method =='POST':
        data = request.form['input_text']
        message = "predicting"
        pred = 'MODEL %s predicted:'%model + '\n' + predict_text(data, model)
        return render_template('index.html', show_pred=1, pred=pred)
    return render_template('index.html', show_pred=0)

if __name__ == '__main__':
    app.run(debug=False)

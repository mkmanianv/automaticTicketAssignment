from flask import Flask, request, jsonify

import numpy as np
import joblib
from pickle import load

from PreProcessing import PreProcessing

application = Flask(__name__)

clf = joblib.load("Automatic_Ticket_Assignment_Capstone_Project.joblib")
le = load(open('classes.pkl', 'rb'))

def readRequest(text):
    preprocessing = PreProcessing()
    clean_text = preprocessing.data_clean(text)
    predict_value = clf.predict_proba([clean_text])
    maxValue=np.amax(predict_value)
    argMax = np.argmax(predict_value)
    if(maxValue>0.5):
        return "Your ticket is assigned to: "+le.inverse_transform([argMax])[0]
    else:
        return "Your ticket is assigned to: OTHERS"


@application.route('/ticketclassification', methods=['POST', 'GET'])
def TicketClassification():
    param = (request.args.get('input', None))
    rt = readRequest(param)
    return jsonify(rt)


if __name__ == '__main__':
    application.run(host="0.0.0.0", port=9052, debug=False)

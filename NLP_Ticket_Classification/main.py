from flask import Flask,request,Response, jsonify
from joblib import load

from PreProcessing import PreProcessing

application = Flask(__name__)

# pipeline = load("text_classification_spyder.joblib")

def readRequest(text):
    label = 0
    dictionary = {}
    # label = pipeline.predict(text)[0]
    preprocessing = PreProcessing()
    return preprocessing.data_clean(text)
    # if label == 0:
    #     dictionary.update({"Sentiment of tweet is": "Positive"})
    #
    # else:
    #     dictionary.update({"Sentiment of tweet is": "Negative"})
    #
    # return dictionary

@application.route('/ticketclassification', methods=['POST', 'GET'])
def TicketClassification():
    param = (request.args.get('input', None))
    rt = readRequest(param)
    return jsonify(rt)



if __name__ == '__main__':
    application.run(host="0.0.0.0",port=9052,debug=False)


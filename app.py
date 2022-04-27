"""
A sample Hello World server.
"""
import os

from flask import Flask, render_template, jsonify
from flask_cors import CORS

# pylint: disable=C0103
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    message = "It's running!"

    """Get Cloud Run environment variables."""
    service = os.environ.get('K_SERVICE', 'Unknown service')
    revision = os.environ.get('K_REVISION', 'Unknown revision')

    return render_template('index.html',
        message=message,
        Service=service,
        Revision=revision)



@app.route('/check-transaction')
def is_fraud_transaction():
    
    csvLine="476,-0.867554210779743,-0.418633339430195,2.29492668654691,0.219869661334528,-0.0858203228696113,-0.839204425847823,-0.724947469291827,0.221811953674263,0.42373813393856,-0.431875702661519,-0.867638465112668,-0.486136976299496,-0.799464938201214,-0.16908491079299,0.963012475970998,0.0132524792749653,0.0728621623379799,0.287711892207123,0.78858803260512,0.226694125853925,0.231306350183918,0.547469818349216,-0.00160817851451261,0.461130993390382,-0.504833531557196,1.14669171392115,0.0616510209699604,0.146243502211805,1"

    modelFileName="storedModel.pckl"

    # load the model from disk
    loaded_model = pickle.load(open(modelFileName, 'rb'))

    # Header line
    csvHeader="""Time,V1,V2,V3,V4,V5,V6,V7,V8,V9,V10,V11,V12,V13,V14,V15,V16,V17,V18,V19,V20,V21,V22,V23,V24,V25,V26,V27,V28,Amount
    """

    # Create datafile
    TESTDATA=csvHeader+"\n"+csvLine
    df = pd.read_csv(io.StringIO(TESTDATA), sep=",")

    # Prepare scaler
    sc=StandardScaler()
    sc.set_params(**{'copy': True, 'with_mean': True, 'with_std': True})

    # Transform ammount column
    df['normAmount'] = sc.fit_transform(df['Amount'].values.reshape (-1,1))

    # Remove not needed columns
    df = df.drop (['Time', 'Amount'], axis = 1);

    # load the model from disk
    loaded_model = pickle.load(open(modelFileName, 'rb'))
    result1 = loaded_model.predict(df.iloc[[0]])[0]
    

    result = {"result":'OK' if result1 == 0 else 'FRAUD'}
    return jsonify(result)
        

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')

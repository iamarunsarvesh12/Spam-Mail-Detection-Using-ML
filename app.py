from flask import Flask, render_template, request, jsonify
from predict import predict_message

app = Flask(__name__)

@app.route('/')
def home():
    # Shows the main HTML page
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Gets the message from frontend
    data = request.get_json()
    message = data.get('message', '')
    
    if not message.strip():
        return jsonify({'error': 'Message cannot be empty'}), 400

    try:
        # Passes message to your existing ML logic
        result = predict_message(message)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
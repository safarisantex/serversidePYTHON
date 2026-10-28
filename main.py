from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import json

app = Flask(__name__)

# Allow cross-origin requests from any frontend domain
CORS(app, resources={r"/*": {"origins": "*"}})

# CRITICAL: This secret key must perfectly match your frontend JavaScript key
SECRET_KEY = "MySuperSecretKey123" 

def xor_decrypt(encrypted_bytes, key):
    """Reverses the frontend XOR character scrambling operation"""
    decrypted_chars = []
    key_length = len(key)
    
    for index, byte in enumerate(encrypted_bytes):
        # Apply the bitwise XOR operator to reverse the encryption
        decrypted_chars.append(chr(byte ^ ord(key[index % key_length])))
        
    return "".join(decrypted_chars)

@app.route('/', methods=['POST', 'OPTIONS'])
def handle_submission():
    if request.method == 'POST':
        try:
            # 1. Capture the raw text body payload sent by the browser fetch request
            scrambled_payload = request.data.decode('utf-8')
            
            # 2. Decode the Base64 layer back into raw encrypted bytes
            encrypted_bytes = base64.b64decode(scrambled_payload)
            
            # 3. Descramble the bytes using the matching XOR secret key
            json_string = xor_decrypt(encrypted_bytes, SECRET_KEY)
            
            # 4. Convert the decoded JSON text string into a native Python dictionary
            form_data = json.loads(json_string)
            
            # Log the data securely to your server terminal output
            print("Successfully Decoded Payload:", form_data)
            
            # 5. Reply to the frontend browser to confirm safe reception
            return jsonify({"status": "success", "message": "Data received and decoded."}), 200
            
        except Exception as error:
            print("Decoding Error Encountered:", str(error))
            return jsonify({"status": "error", "message": "Invalid payload format."}), 400

if __name__ == '__main__':
    # Default port environment used during local machine testing
    app.run(host='0.0.0.0', port=5000)

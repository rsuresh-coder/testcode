from datetime import datetime as time
from transformers import pipeline
from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
from flask_ngrok import run_with_ngrok

# Initialize the translation model and tokenizer
translator = pipeline("translation_en_to_es", model="Helsinki-NLP/opus-mt-en-es") #, device=0)

@app.route('/translate', methods=['POST'])
def translate_text():
    # Get the text from the request JSON
    data = request.get_json(force=True)
    text = data.get("text")
    
    # Check if text was provided
    if not text:
        return jsonify({"error": "No text provided for translation."}), 400
    
    try:
        # Translate the text
        prevTime = time.now()
        translation = translator(text, max_length=512)
        translated_text = translation[0]['translation_text']
        print(f"translation over, time: {time.now() - prevTime}")

        return jsonify({"translated_text": translated_text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)
    
    
from threading import Thread

def run_app():
    app.run()

Thread(target=run_app).start()
    
# input_text = "Our customer can only communicate in Spanish. If you prefer talking in English please you speak now but don't be long. It would be translated to Spanish and played back to the banker. Our customer can only communicate in Spanish. If you prefer talking in English please you speak now but don't be long. It would be translated to Spanish and played back to the banker. Our customer can only communicate in Spanish. If you prefer talking in English please you speak now but don't be long. It would be translated to Spanish and played back to the banker."

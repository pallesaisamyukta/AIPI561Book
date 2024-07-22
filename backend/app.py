from flask import Flask, request, jsonify
from flask_cors import CORS
from summary import Summarizer

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Hello World"

@app.route("/test", methods=['POST'])
def test():
    print("Received request at /test endpoint")
    return jsonify({"response": "Hello from /test endpoint"})

@app.route('/summarize', methods=['POST'])
def summarize():
    """
    API endpoint to summarize PDF text.
    Expects JSON input with 'pdf_path' as the path to the PDF file.
    Returns a JSON response with the 'summary'.
    """
    print("Received request at /summarize endpoint")
    data = request.get_json()
    pdf_path = data.get('pdf_path')
    print(f"Received request to summarize PDF: {pdf_path}")

    try:
        summarizer = Summarizer()
        summary_text = summarizer.summarize_pdf_parallel(pdf_path)
        print(f"Generated summary for {pdf_path}:\n{summary_text}")
        return jsonify({'summary': summary_text})
    except Exception as e:
        print(f"Error during summarization: {e}")
        return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True, port=5050)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)

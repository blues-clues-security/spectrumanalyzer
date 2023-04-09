from flask import Flask, render_template, request, jsonify
from spectrum_analyzer import SpectrumAnalyzer
import base64
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/options', methods=['POST'])
def options():
    options_data = request.get_json()
    # Process the options_data and create a SpectrumAnalyzer instance with the given options
    analyzer = SpectrumAnalyzer(options_data)

    # Get the generated image and convert it to base64
    buf = io.BytesIO()
    analyzer.fig.savefig(buf, format='png')
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')

    return jsonify({'image': image_base64})

if __name__ == '__main__':
    app.run(debug=True)
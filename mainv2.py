from flask import Flask, request, send_file, jsonify
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

@app.route('/remove-background', methods=['POST'])
def remove_background():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    input_image = file.read()


    input_stream = io.BytesIO(input_image)
    image = Image.open(input_stream)


    if image.mode == 'RGBA' or (image.mode == 'LA' and 'A' in image.getbands()):
     
        input_stream.seek(0)
        return send_file(
            input_stream,
            mimetype='image/png',
            as_attachment=True,
            download_name='output_image.png'
        )


    output_image = remove(input_image)


    output_stream = io.BytesIO(output_image)
    output_stream.seek(0)

    return send_file(
        output_stream,
        mimetype='image/png',
        as_attachment=True,
        download_name='output_image.png'
    )

if __name__ == '__main__':
    app.run(debug=True)

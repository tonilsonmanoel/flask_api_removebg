
import random
import string
from flask import Flask, request, jsonify, send_from_directory
from rembg import remove
from PIL import Image
import os
import io

app = Flask(__name__)

def geradorStringAletorio(tamanho):
    stringAletorio = string.ascii_letters + string.digits
    return ''.join(random.choice(stringAletorio) for _ in range(tamanho))

# Diretório onde as imagens serão salvas temporariamente
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Rota para receber a imagem via POST
@app.route('/remove_background', methods=['POST'])
def remove_background():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        # Salvar a imagem temporariamente
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)

        # Remover o fundo da imagem
        randomString = geradorStringAletorio(16)
        output_filename = os.path.join(UPLOAD_FOLDER, 'removed_bg_' + randomString+".png")
        img_caminho = 'removed_bg_' + randomString+".png"
        with open(filename, "rb") as f_img:
            img = Image.open(f_img)
            img = remove(img)
            img.save(output_filename)

        return jsonify({'image_url': request.host_url + 'view_removed_bg/' + img_caminho})

# Rota para visualizar a imagem removida do fundo
@app.route('/view_removed_bg/<filename>')
def view_removed_background(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run()
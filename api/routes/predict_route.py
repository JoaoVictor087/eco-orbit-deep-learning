from flask import Blueprint, request, jsonify
from api.config import allowed_file
from api.services.inference_service import EcoOrbitModel
from werkzeug.utils import secure_filename

predict_bp = Blueprint('predict_bp', __name__)


@predict_bp.route('/predict', methods=['POST'])
def handle_prediction():
    if 'imagem' not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado. Use o campo 'imagem'."}), 400

    arquivo = request.files['imagem']

    if arquivo.filename == '':
        return jsonify({"erro": "Nome de arquivo inválido ou arquivo vazio."}), 400

    if not allowed_file(arquivo.filename):
        return jsonify({"erro": "Formato de arquivo não permitido. Use JPG ou PNG."}), 415

    try:
        nome_seguro = secure_filename(arquivo.filename)

        image_bytes = arquivo.read()

        resultado = EcoOrbitModel.prever(image_bytes)

        resultado["arquivo_analisado"] = nome_seguro
        return jsonify(resultado), 200

    except RuntimeError as re:
        return jsonify({"erro": str(re)}), 500
    except Exception as e:
        return jsonify({"erro": "Falha interna no servidor."}), 500
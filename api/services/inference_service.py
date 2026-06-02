import os
import io
import tensorflow as tf
from PIL import Image
from api.config import Config

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class EcoOrbitModel:
    _modelo = None

    @classmethod
    def get_model(cls):
        if cls._modelo is None:
            if not os.path.exists(Config.MODEL_PATH):
                raise FileNotFoundError(f"Modelo não encontrado em: {Config.MODEL_PATH}")
            cls._modelo = tf.keras.models.load_model(Config.MODEL_PATH)
            print("Modelo carregado com sucesso!")
        return cls._modelo

    @classmethod
    def prever(cls, image_bytes: bytes) -> dict:
        try:
            img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            img = img.resize((224, 224))

            img_array = tf.keras.utils.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)

            modelo = cls.get_model()
            previsao = modelo.predict(img_array, verbose=0)
            probabilidade = float(previsao[0][0])

            fogo_detectado = probabilidade > 0.5
            confianca = probabilidade if fogo_detectado else (1.0 - probabilidade)

            return {
                "fogo_detectado": fogo_detectado,
                "confianca_percentual": round(confianca * 100, 2)
            }

        except Exception as e:
            raise RuntimeError(f"Erro ao processar o tensor: {str(e)}")
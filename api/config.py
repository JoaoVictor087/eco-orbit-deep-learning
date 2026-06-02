import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    MODEL_PATH = os.path.join(BASE_DIR, 'models', 'modelo_wildfire.keras')

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
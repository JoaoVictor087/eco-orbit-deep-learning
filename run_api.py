from api.app import create_app
from api.services.inference_service import EcoOrbitModel

app = create_app()

if __name__ == '__main__':
    try:
        EcoOrbitModel.get_model()
    except FileNotFoundError as e:
        print(f"ERRO FATAL: {e}")
        exit(1)

    app.run(host='0.0.0.0', port=5000, debug=False)
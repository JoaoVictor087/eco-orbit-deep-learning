import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from PIL import Image, ImageDraw

TAMANHO_JANELA = 224

print("Carregando modelo EcoOrbit...")
modelo = tf.keras.models.load_model('models/modelo_wildfire.keras')
print("Modelo carregado.")


def escanear_imagem_satelite(caminho_imagem, caminho_saida):
    print(f"\n🌍 Abrindo imagem de satélite: {caminho_imagem}")
    try:
        img_original = Image.open(caminho_imagem).convert('RGB')
        largura, altura = img_original.size

        img_desenho = img_original.copy()
        draw = ImageDraw.Draw(img_desenho, "RGBA")

        focos_encontrados = 0
        total_janelas = 0

        print(f"Resolução original: {largura}x{altura}")
        print("Iniciando varredura por quadrantes...\n")

        for y in range(0, altura, TAMANHO_JANELA):
            for x in range(0, largura, TAMANHO_JANELA):
                box = (x, y, x + TAMANHO_JANELA, y + TAMANHO_JANELA)
                tile = img_original.crop(box)

                if tile.size != (TAMANHO_JANELA, TAMANHO_JANELA):
                    tile = tile.resize((TAMANHO_JANELA, TAMANHO_JANELA))

                img_array = tf.keras.utils.img_to_array(tile)
                img_array = tf.expand_dims(img_array, 0)

                previsao = modelo.predict(img_array, verbose=0)
                probabilidade = previsao[0][0]

                total_janelas += 1

                if probabilidade > 0.5:
                    focos_encontrados += 1
                    draw.rectangle(box, fill=(255, 0, 0, 100), outline="red", width=3)
                    print(f"ALERTA: Foco detectado na região (X:{x}, Y:{y}) - Confiança: {probabilidade:.1%}")

        img_desenho.save(caminho_saida)

        print(f"\n Relatório Final:")
        print(f"Total de áreas analisadas: {total_janelas}")
        print(f"Focos de incêndio marcados: {focos_encontrados}")
        print(f"Mapa salvo com marcações em: {caminho_saida}")

    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")


if __name__ == "__main__":
    imagem_entrada = "image_tests/snapshot-2019-09-07.jpg"
    imagem_saida = "analises/analise-snapshot-2019-09-07.jpg"

    if os.path.exists(imagem_entrada):
        escanear_imagem_satelite(imagem_entrada, imagem_saida)
    else:
        print(f"Imagem '{imagem_entrada}' não encontrada. Salve o link da NASA nesta pasta com esse nome!")
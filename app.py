import os
import re
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png'}


def alphanumeric_key(filename):
    parts = re.split(r'(\d+)', filename)
    return [int(part) if part.isdigit() else part.lower() for part in parts]


def locate_fotos_folder():
    static_dir = os.path.join(app.root_path, 'static')
    for folder_name in ['Fotos', 'fotos']:
        candidate = os.path.join(static_dir, folder_name)
        if os.path.isdir(candidate):
            return candidate, folder_name
    return os.path.join(static_dir, 'Fotos'), 'Fotos'


def load_gallery_images():
    folder_path, folder_name = locate_fotos_folder()
    images = [
        filename
        for filename in os.listdir(folder_path)
        if os.path.splitext(filename)[1].lower() in IMAGE_EXTENSIONS
    ]
    images.sort(key=alphanumeric_key)
    return images, folder_name


def carta_text_path():
    return os.path.join(app.root_path, 'carta.txt')


def load_carta_text():
    path = carta_text_path()
    if os.path.isfile(path):
        with open(path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    return 'Mi amor, cada día a tu lado es un regalo.\nTe amo con todo mi corazón.'


def save_carta_text(texto):
    path = carta_text_path()
    with open(path, 'w', encoding='utf-8') as file:
        file.write(texto.strip())


@app.route('/')
def home():
    fotos, fotos_folder = load_gallery_images()
    midpoint = (len(fotos) + 1) // 2
    fotos_bloque1 = fotos[:midpoint]
    fotos_bloque2 = fotos[midpoint:]

    return render_template(
        'index.html',
        pareja1='Tu Nombre',
        pareja2='Su Nombre',
        fecha_aniversario='16 de Junio',
        fotos_bloque1=fotos_bloque1,
        fotos_bloque2=fotos_bloque2,
        fotos_folder=fotos_folder,
    )


@app.route('/carta', methods=['GET', 'POST'])
def carta():
    if request.method == 'POST':
        carta_texto = request.form.get('carta_texto', '').strip()
        if carta_texto:
            save_carta_text(carta_texto)
        return redirect(url_for('carta'))

    carta_texto = load_carta_text()
    return render_template('carta.html', carta_texto=carta_texto)


if __name__ == '__main__':
    app.run(debug=True)

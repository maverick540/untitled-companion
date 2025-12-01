import os
from PIL import Image

# Carpeta donde buscar las imágenes
IMAGE_FOLDER = "game/images"

TARGET_HEIGHT = 720  # Solo fijamos la altura

def is_bg_file(filename):
    lower = filename.lower()
    return (lower.startswith("sprite") or lower.startswith("eileen")) and lower.endswith((".png", ".jpg", ".jpeg", ".webp"))

def resize_image(path):
    try:
        img = Image.open(path)
        w, h = img.size

        # Calcular nuevo ancho manteniendo aspecto
        scale = TARGET_HEIGHT / float(h)
        new_width = int(w * scale)

        img = img.resize((new_width, TARGET_HEIGHT), Image.LANCZOS)
        img.save(path)

        print(f"✔ Redimensionado: {path}  → {new_width}x{TARGET_HEIGHT}")
    except Exception as e:
        print(f"✘ Error con {path}: {e}")

def process_folder(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            if is_bg_file(file):
                full_path = os.path.join(root, file)
                resize_image(full_path)

if __name__ == "__main__":
    print("Buscando fondos que comiencen con 'bg' en game/images…")
    process_folder(IMAGE_FOLDER)
    print("Proceso terminado.")

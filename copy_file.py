import shutil

from display_message import display_message


def copy_file(origin_path, destiny_path):
    try:
        shutil.copyfile(origin_path, destiny_path)
        display_message(f"Arquivo copiado com sucesso para {destiny_path}")
    except Exception as e:
        display_message(f"Erro ao copiar arquivo: {str(e)}")
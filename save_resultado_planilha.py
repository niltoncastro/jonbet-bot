import os
from datetime import datetime

from copy_file import copy_file
from display_message import display_message
from openpyxl import load_workbook

from mappings import paths


def save_planlha_resultado_final(nome_planilha, ultimo_id, time_casa, placar_casa, time_visitante, placar_visitante):
    local_path = paths("file_server_local")
    gdrive_path = paths("file_server_gdrive")

    try:
        planilha_gdrive_path = gdrive_path + nome_planilha
        planilha_local_path = local_path + nome_planilha

        # Carregar a planilha existente
        if os.path.exists(planilha_gdrive_path):
            workbook = load_workbook(planilha_gdrive_path)
        else:
            display_message(f"Erro: Planilha {planilha_gdrive_path} não encontrada.")
            return

        # Selecionar as abas
        sheet_name_resultados = "Resultados"  # Defina o nome da aba que você deseja selecionar

        if sheet_name_resultados in workbook.sheetnames:
            sheet_resultados = workbook[sheet_name_resultados]
        else:
            display_message(f"Aba {sheet_name_resultados} não encontrada. Criando nova aba.")
            sheet_resultados = workbook.create_sheet(title=sheet_name_resultados)

        # Encontrar a próxima linha vazia
        row = int(ultimo_id) + 1

        # Gravar os dados na próxima linha
        current_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        sheet_resultados[f"B{row}"] = time_casa
        sheet_resultados[f"C{row}"] = placar_casa
        sheet_resultados[f"D{row}"] = placar_visitante
        sheet_resultados[f"E{row}"] = time_visitante
        sheet_resultados[f"G{row}"] = current_time

        # Salvar a planilha
        workbook.save(planilha_gdrive_path)
        display_message(f"Resultados finais gravados na planilha {planilha_gdrive_path} para {time_casa} x {time_visitante}")

        copy_file(planilha_gdrive_path, planilha_local_path)

    except Exception as e:
        display_message(f"Erro ao salvar o resultado na planilha: {str(e)}")

# Caminho do banco de dados
import sqlite3

from display_message import display_message
from log_writer import log_writer

# Caminho do banco de dados
db_path = "C:/Users/junio/AppData/Roaming/DBeaverData/workspace6/jonbet_bot/jonbet-bot"


def insert_resultado(nome_tabela, codigo_partida, codigo_liga, nome_liga, time_casa, placar_casa, time_visitante,
                     placar_visitante, tempo_partida, placar_1T, placar_2T, sigla_estado_partida,
                     descricao_estado_partida, placar_final, flg_final, tipo_resultado, descricao_resultado,
                     resultado_partida, flg_virada, data_partida, data_criacao):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(f"""
        INSERT INTO {nome_tabela} (codigo_partida, codigo_liga, nome_liga, time_casa, placar_casa, time_visitante,
                                      placar_visitante, tempo_partida, placar_1T, placar_2T, sigla_estado_partida, 
                                      descricao_estado_partida, placar_final, flg_final, tipo_resultado, descricao_resultado,
                                      resultado_partida, flg_virada, data_partida, data_criacao)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (codigo_partida, codigo_liga, nome_liga, time_casa, placar_casa, time_visitante,
              placar_visitante, tempo_partida, placar_1T, placar_2T, sigla_estado_partida,
              descricao_estado_partida, placar_final, flg_final, tipo_resultado, descricao_resultado,
              resultado_partida, flg_virada, data_partida, data_criacao))

        conn.commit()
        conn.close()
        # display_message(f"Dados da partida inseridos com sucesso")
    except Exception as e:
        message = f"Erro ao gravar no banco de dados: {str(e)}"
        display_message(message)
        log_writer(message)


def busca_ultimo_id(nome_tabela):
    # print("busca_ultimo_id")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query para buscar o maior ID
        query = f"SELECT COUNT(*) FROM {nome_tabela} WHERE FLG_FINAL = 'S'"
        cursor.execute(query)
        resultado = cursor.fetchone()

        # Verificar se o resultado não é None
        ultimo_id = resultado[0] if resultado[0] is not None else 0

        conn.close()

        # Mensagem de retorno
        # display_message(f"Número do último ID retornado: {ultimo_id}")
        return ultimo_id
    except Exception as e:
        message = f"Erro ao buscar no banco de dados: {str(e)}"
        display_message(message)
        log_writer(message)
        return None

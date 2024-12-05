# Caminho do banco de dados
import sqlite3

from display_message import display_message

# Caminho do banco de dados
db_path = "C:/Users/junio/AppData/Roaming/DBeaverData/workspace6/jonbet_bot/jonbet-bot"


def insert_resultado(codigo_partida, codigo_liga, nome_liga, time_casa, placar_casa, time_visitante,
                     placar_visitante, tempo_partida, placar_1T, placar_2T, sigla_estado_partida,
                     descricao_estado_partida, flg_final, tipo_resultado, descricao_resultado,
                     resultado_partida, flg_virada, data_partida, data_criacao):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO resultados_fifa (codigo_partida, codigo_liga, nome_liga, time_casa, placar_casa, time_visitante,
                                      placar_visitante, tempo_partida, placar_1T, placar_2T, sigla_estado_partida, 
                                      descricao_estado_partida, flg_final, tipo_resultado, descricao_resultado,
                                      resultado_partida, flg_virada, data_partida, data_criacao)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (codigo_partida, codigo_liga, nome_liga, time_casa, placar_casa, time_visitante,
              placar_visitante, tempo_partida, placar_1T, placar_2T, sigla_estado_partida,
              descricao_estado_partida, flg_final, tipo_resultado, descricao_resultado,
              resultado_partida, flg_virada, data_partida, data_criacao))

        conn.commit()
        conn.close()
        display_message(f"Dados da partida a iniciar gravados para  {time_casa} x {time_visitante}")
    except Exception as e:
        display_message(f"Erro ao gravar no banco de dados: {str(e)}")

MENU_PRINCIPAL = """Menu Principal
1 - Relatórios
2 - Inserir Registros
3 - Atualizar Registros
4 - Remover Registros
5 - Sair
"""

MENU_RELATORIOS = """Relatórios
1 - Relatório de Clientes
2 - Relatório de Técnicos
3 - Relatório de Peças
4 - Relatório de Peças Utilizadas
5 - Relatório de Ordens de Serviços 
0 - Sair
"""


MENU_ENTIDADES = """Entidades
1 - CLIENTES
2 - TÉCNICOS
3 - PEÇAS
4 - PEÇAS UTILIZADAS
5 - ORDENS DE SERVIÇO
"""

def queryCount(collection_name):
    from conexion.mongoQueries import MongoQueries
    import pandas as pd

    mongo = MongoQueries()
    mongo.connect()

    myCollection = mongo.db[collection_name]
    totalDocumentos = myCollection.count_documents({})
    mongo.close()

    df = pd.DataFrame({f"total_{collection_name}": [totalDocumentos]})
    return df

def clear_console(wait_time: int=3):
    
    import os
    from time import sleep
    sleep(wait_time)
    os.system('clear')

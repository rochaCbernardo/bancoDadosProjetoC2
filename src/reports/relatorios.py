from conexion.mongoQueries import MongoQueries
import pandas as pd
from pymongo import ASCENDING, DESCENDING

class Relatorio:
    def __init__(self):
        pass

    def get_relatorioClientes(self):

        mongo = MongoQueries()
        mongo.connect()

        query_result = mongo.db["clientes"].find({}, 
                                                 {"cliente_id": 1, 
                                                  "nome": 1,
                                                  "endereco": 1,
                                                  "email": 1,
                                                  "telefone": 1, 
                                                  "_id": 0
                                                 }).sort("nome", ASCENDING)
        dfCliente = pd.DataFrame(list(query_result))
        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(dfCliente)
        input("Pressione Enter para Sair do Relatório de Clientes..")

    def get_relatorioTecnicos(self):

        mongo = MongoQueries()
        mongo.connect()

        query_result = mongo.db["tecnicos"].find({}, 
                                                 {"tecnico_id": 1, 
                                                  "nome": 1,
                                                  "especialidade": 1,
                                                  "telefone": 1,
                                                  "valor_os": 1, 
                                                  "_id": 0
                                                 }).sort("nome", ASCENDING)
        dfTecnico = pd.DataFrame(list(query_result))
        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(dfTecnico)
        input("Pressione Enter para Sair do Relatório de Tecnicos..")

    def get_relatorioPecas(self):

        mongo = MongoQueries()
        mongo.connect()

        query_result = mongo.db["pecas"].find({},
                                             {"peca_id": 1,
                                              "nome": 1,
                                              "preco_uni": 1,
                                              "_id": 0})
        dfPeca = pd.DataFrame(list(query_result))

        mongo.close()

        print(dfPeca)
        input("Pressione Enter para Sair do Relatório de Peças..")

    def get_relatorioOsConsolidado(self):
        mongo = MongoQueries()
        mongo.connect()

        query_result = mongo.db["ordens_servico"].aggregate([{'$lookup':{'from':'clientes',
                                                                        'localField': 'cliente_id',
                                                                        'foreignField': 'cliente_id',
                                                                        'as': 'cliente_id'
                                                                        }
                                                                    },
                                                                    {
                                                                        '$unwind': {'path': '$cliente_id'}
                                                                    },
                                                                    {
                                                                        '$lookup':{'from': 'tecnicos',
                                                                                   'localField': 'tecnico_id',
                                                                                   'foreignField': 'tecnico_id',
                                                                                   'as': 'tecnico_id'}
                                                                    },
                                                                    {
                                                                        '$unwind': {'path': '$tecnico_id'}
                                                                    },
                                                                    {
                                                                        '$lookup':{
                                                                            'from': 'pecas_utilizadas',
                                                                            'localField': 'codigo',
                                                                            'foreignField': 'cod_peca_utilizada',
                                                                            'as': 'cod_peca_utilizada'
                                                                        }
                                                                    },
                                                                    {
                                                                        '$unwind':{'path': '$cod_peca_utilizada'}
                                                                    },
                                                                    {
                                                                        '$project':{                                                               
                                                                        'ordem_id': 1,
                                                                        'cliente': "$cliente_id.nome",
                                                                        'tecnico': "$tecnico_id.nome",
                                                                        'cod_peca_utilizada': "$cod_peca_utilizada.codigo",
                                                                        'data_abertura': 1,
                                                                        'data_conclusao': 1,
                                                                        'status_os': 1,
                                                                        'valor_tecnico': "$tecnico_id.valor_os",
                                                                        'custo_toal': 1,
                                                                        '_id':0
                                                                        }
                                                                    }])
        dfOsConsolidada = pd.DataFrame(list(query_result))

        mongo.close()

        print(dfOsConsolidada[["ordem_id", "cliente", "tecnico", "cod_peca_utilizada", "data_abertura", "data_conclusao", "status_os", "valor_tecnico", "custo_total"]])
        input("Pressione Enter para Sair do Relatório de OS consolidadas..")

    def get_relatorioPecasUtilizadas(self):
        mongo = MongoQueries()
        mongo.connect()

        query_result = mongo.db["pecas_utilizadas"].aggregate([{
                                                                '$lookup':{'from': "pecas",
                                                                           'localField': "peca_id",'foreignField': "peca_id",'as': "peca_id"
                                                                           }
                                                                           },
                                                                           {
                                                                        '$unwind': {'path': '$peca_id'}
                                                                            },
                                                                           {
                                                                               '$project':
                                                                               {
                                                                               'codigo': 1,
                                                                               'peca_id': '$peca_id.peca_id',
                                                                               'nome': '$peca_id.nome',
                                                                               'valor_peca': '$peca_id.preco_uni',
                                                                               'quant_utilizada': 1,
                                                                               'valor_total_pecas': {'$multiply':["$quant_utilizada", "$peca_id.preco_uni"]},
                                                                               '_id': 0
                                                                               }
                                                                            }])
        dfPecaUtilizada = pd.DataFrame(list(query_result))
        mongo.close()

        print(dfPecaUtilizada[["codigo", "peca_id", "nome", "valor_peca", "quant_utilizada", "valor_total_pecas"]])
        input("Pressione Enter para Sair do Relatório de Peças Utilizadas..")

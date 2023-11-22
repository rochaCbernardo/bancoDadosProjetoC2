from model.pecas import Peca
from conexion.mongoQueries import MongoQueries
import pandas as pd

class ControllerPeca:
    def __init__(self):
        self.mongo = MongoQueries()

    def inserirPeca(self) -> Peca:

        self.mongo.connect()

        peca_id = int(input("Informe o ID da peça que será cadastrada: "))

        if self.verificaExistenciaPeca(peca_id):
            nome = input("Nome da peça: ")
            preco_uni = input("Preço unitário: ")

            self.mongo.db["peca"].insert_one({"peca_id": peca_id, "nome": nome, "preco_uni": preco_uni})

            dfPeca = self.recuperaPeca(peca_id)

            novaPeca = Peca(dfPeca.peca_id.values[0], dfPeca.nome.values[0], dfPeca.preco_uni.values[0])

            print(novaPeca.to_String())
            self.mongo.close()
            return novaPeca

        else:
            self.mongo.close()
            print(f"O ID {peca_id} já foi cadastrado em sistema.")
            return None

    def atualizarPeca(self) -> Peca:
        self.mongo.connect()

        peca_id = int(input("Informe o ID da peça que será atualizada: "))

        if not self.verificaExistenciaPeca(peca_id):
            novo_nome = input("Novo nome da peça: ")
            novo_preco_uni = input("Novo preço unitário: ")

            self.mongo.db["peca"].update_one({"peca_id": peca_id}, {"$set":{"nome": novo_nome, "preco_uni": novo_preco_uni}})

            dfPeca = self.recuperaPeca(peca_id)

            pecaAlterada = Peca(dfPeca.peca_id.values[0], dfPeca.nome.values[0], dfPeca.preco_uni.values[0])

            print(pecaAlterada.to_String())
            self.mongo.close()

            return pecaAlterada
        else:
            self.mongo.close()
            print(f"O ID {peca_id} não está cadastrado em sistema.")
            return None

    def excluirPeca(self) -> Peca:
        self.mongo.connect()

        peca_id = int(input("Informe o ID da peça que será excluída: "))

        if not self.verificaExistenciaPeca(peca_id):
            dfPeca = self.recuperaPeca(peca_id)

            self.mongo.db["peca"].delete_one({"peca_id": peca_id})

            pecaExcluida = Peca(dfPeca.peca_id.values[0], dfPeca.nome.values[0], dfPeca.preco_uni.values[0])
            self.mongo.close()

            print("Peça excluída com sucesso!")
            print(pecaExcluida.to_String())

        else:
            self.mongo.close()
            print(f"O ID {peca_id} não está cadastrado em sistema.")

    def verificaExistenciaPeca(self, peca_id: int = None, external:bool=False) -> bool:
        if external:
            self.mongo.connect()

        dfPeca = pd.DataFrame(self.mongo.db["peca"].find({"peca_id": peca_id}, {"peca_id": 1, "nome": 1, "preco_uni": 1}))

        if external:
            self.mongo.close()

        return dfPeca.empty

    def recuperaPeca(self, peca_id: int = None, external:bool=False) -> pd.DataFrame:
        if external:
            self.mongo.connect()

        dfPeca = pd.DataFrame(list(self.mongo.db["peca"].find({"peca_id": peca_id}, {"peca_id": 1, "nome": 1, "preco_uni": 1})))

        if external:
            self.mongo.close()

        return dfPeca
import pandas as pd
from conexion.mongoQueries import MongoQueries
from controller.controller_pecas import ControllerPeca
from model.pecas import Peca
from model.pecas_utilizadas import PecaUtilizada
from reports.relatorios import Relatorio


class ControllerPecasUtilizadas:
    def __init__(self):
        self.mongo = MongoQueries()
        self.ctrlPeca = ControllerPeca()
        self.relatorios = Relatorio()

    def cadastrarPecaUtilizada(self) -> PecaUtilizada:
        self.mongo.connect()

        peca_id = int(input("Informe o ID da peça utilizada: "))
        peca = self.validaPeca(peca_id)
        if peca == None:
            return None
        
        codigo = int(input("Informe o código do conjuto de peças utilizadas: "))

        if self.verificaExistenciaPecaUtilizada(codigo):
        
            quant_utilizada = int(input("Informe a quantidade utilizada: "))

            data = dict(codigo = codigo, peca_id=int(peca.get_peca_id()), quant_utilizada=quant_utilizada)

            self.mongo.db["pecas_utilizadas"].insert_one(data)

            dfPecaUtilizada = self.recuperaPecaUtilizada(codigo)
        
            novaPecaUtilizada = PecaUtilizada(dfPecaUtilizada.codigo.values[0], dfPecaUtilizada.peca_id.values[0], dfPecaUtilizada.quant_utilizada.values[0])

            print(novaPecaUtilizada.to_String())
            self.mongo.close()

            return novaPecaUtilizada
        else:
            self.mongo.close()
            print(f"O código {codigo}, já foi cadastrado em sistema.")
            return None

    def atualizarPecaUtilizada(self) -> PecaUtilizada:
        self.mongo.connect()

        codigo = int(input("Informe o do conjuto de peças utilizadas que será atualizado: "))

        if not self.verificaExistenciaPecaUtilizada(codigo):

            self.relatorios.get_relatorioPecas()
            peca_id = int(input("Digite o ID da peça: "))

            peca = self.validaPeca(peca_id)
            if peca == None:
                return None

            quant_utilizada = int(input("Informe a quantidade utilizada: "))

            self.mongo.db["pecas_utilizadas"].update_one({"codigo": codigo}, {"$set": {"peca_id": int(peca.get_peca_id()), "quant_utilizada": quant_utilizada}})

            dfPecaUtilizada = self.recuperaPecaUtilizada(codigo)

            pecaUtilizadaAtualizada = PecaUtilizada(dfPecaUtilizada.codigo.values[0], dfPecaUtilizada.peca_id.values[0], dfPecaUtilizada.quant_utilizada.values[0])

            print(pecaUtilizadaAtualizada.to_String())

            return pecaUtilizadaAtualizada
        else:
            self.mongo.close()
            print(f"O código {codigo} não existe.")
            return None

    def excluirPecasUtilizadas(self) -> PecaUtilizada:
        self.mongo.connect()

        codigo = int(input("Informe o do conjuto de peças utilizadas que será excluído: "))

        if not self.verificaExistenciaPecaUtilizada(codigo):
            dfPecaUtilizada = self.recuperaPecaUtilizada(codigo)
            peca = self.validaPeca(int(dfPecaUtilizada.peca_id.values[0]))

            opcaoExcluir = input(f"Tem certeza que deseja excluir o conjunto de peças ID {codigo}? (S |N) ").upper()
            if opcaoExcluir == "S":
                self.mongo.db["pecas_utilizadas"].delete_one({"codigo": codigo})
                pecaUtilizadaExcluida = PecaUtilizada(dfPecaUtilizada.codigo.values[0], dfPecaUtilizada.peca_id.values[0], dfPecaUtilizada.quant_utilizada.values[0])
                self.mongo.close()

                print("Conjunto removido com sucesso!")
                print(pecaUtilizadaExcluida.to_String())
        else:
            self.mongo.close()
            print(f"O ID {codigo} não existe.")

    def verificaExistenciaPecaUtilizada(self, codigo: int = None, external:bool=False) -> bool:
        if external:
            self.mongo.connect()

        dfPecaUtilizada = pd.DataFrame(self.mongo.db["pecas_utilizadas"].find({"codigo": codigo}, {"codigo": 1, "peca_id": 1, "quant_utilizada": 1}))

        if external:
            self.mongo.close()

        return dfPecaUtilizada.empty

    def recuperaPecaUtilizada(self, codigo:int = None, external:bool = False) -> pd.DataFrame:
        if external:
            self.mongo.connect()

        dfPecaUtilizada = pd.DataFrame(list(self.mongo.db["pecas_utilizadas"].find({"codigo": codigo}, {"codigo": 1, "peca_id": 1, "quant_utilizada": 1})))

        if external:
            self.mongo.close()

        return dfPecaUtilizada

    def validaPeca(self, peca_id: int = None) -> Peca:
        if self.ctrlPeca.verificaExistenciaPeca(peca_id, external=True):
            print(f"A peça buscada {peca_id}, não existe na base.")
            return None
        else:
            dfPeca = self.ctrlPeca.recuperaPeca(peca_id, external=True)
            peca = Peca(dfPeca.peca_id.values[0], dfPeca.nome.values[0], dfPeca.preco_uni.values[0])
            return peca

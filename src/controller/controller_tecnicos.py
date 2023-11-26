import pandas as pd
from model.tecnicos import Tecnico
from conexion.mongoQueries import MongoQueries


class ControllerTecnico:
    def __init__(self):
        self.mongo = MongoQueries()

    def inserirTecnico(self) -> Tecnico:

        self.mongo.connect()

        tecnico_id = int(input("Informe o ID do técnico que será cadastrado: "))

        if self.verificaExistenciaTecnico(tecnico_id):
            nome = input("Nome: ")
            especialidade = input("Especialidade: ")
            email = input("E-mail: ")
            telefone = input("Telefone: ")

            self.mongo.db["tecnicos"].insert_one({"tecnico_id": tecnico_id, "nome": nome, "especialidade": especialidade, "email": email, "telefone": telefone})

            dfTecnico = self.recuperaTecnico(tecnico_id)

            novoTecnico = Tecnico(dfTecnico.tecnico_id.values[0], dfTecnico.nome.values[0], dfTecnico.especialidade.values[0], dfTecnico.email.values[0], dfTecnico.telefone.values[0])

            print(novoTecnico.to_String())
            self.mongo.close()
            return novoTecnico
        else:
            self.mongo.close()
            print(f"O ID {tecnico_id} já está cadastrado para um técnico.")
            return None

    def atualizarTecnico(self) -> Tecnico:

        self.mongo.connect()

        tecnico_id = int(input("Informe o ID do técnico que terá os dados atualizados: "))

        if not self.verificaExistenciaTecnico(tecnico_id):
            novo_nome = input("Novo nome: ")
            nova_especialidade = input("Atualização de especialidade: ")
            novo_email = input("Novo e-mail: ")
            novo_telefone = input("Novo telefone: ")

            self.mongo.db["tecnicos"].update_one({"tecnico_id": tecnico_id}, {"$set": {"nome": novo_nome, "especialidade": nova_especialidade, "email": novo_email, "telefone": novo_telefone}})

            dfTecnico = self.recuperaTecnico(tecnico_id)

            tecnicoAtualizado = Tecnico(dfTecnico.tecnico_id.values[0], dfTecnico.nome.values[0], dfTecnico.especialidade.values[0], dfTecnico.email.values[0], dfTecnico.telefone.values[0])

            print(tecnicoAtualizado.to_String())
            self.mongo.close()
            return tecnicoAtualizado
        else:
            self.mongo.close()
            print(f"O ID {tecnico_id} não foi encontrado em sistema para atualização.")
            return None

    def excluirTecnico(self):

        self.mongo.connect()

        tecnico_id = int(input("Informe o ID do técnico que terá os dados excluídos: "))

        if not self.verificaExistenciaTecnico(tecnico_id):

            dfTecnico = self.recuperaTecnico(tecnico_id)

            opcaoExcluir = input(f"Tem certeza que deseja excluir o conjunto de peças ID {tecnico_id}? (S |N) ").upper()
            if opcaoExcluir == "S":
                self.mongo.db["tecnicos"].delete_one({"tecnico_id": tecnico_id})

                tecnicoExcluido = Tecnico(dfTecnico.tecnico_id.values[0], dfTecnico.nome.values[0],     dfTecnico.especialidade.values[0], dfTecnico.email.values[0], dfTecnico.telefone.values[0])
                self.mongo.close()

                print("Tecnico excluído com sucesso!")
                print(tecnicoExcluido.to_String())

        else:
            self.mongo.close()
            print(f"O ID {tecnico_id} não foi encontrado em sistema para exclusão.")

    def verificaExistenciaTecnico(self, tecnico_id: int = None, external=False) -> bool:
        if external:
            self.mongo.connect()

        dfTecnico = pd.DataFrame(self.mongo.db["tecnicos"].find({"tecnico_id": tecnico_id}, {"tecnico_id": 1, "nome": 1, "especialidade": 1, "email": 1, "telefone": 1, "_id": 0}))

        if external:
            self.mongo.close()

        return dfTecnico.empty

    def recuperaTecnico(self, tecnico_id: int = None, external:bool=False) -> pd.DataFrame:
        if external:
            self.mongo.connect()

        dfTecnico = pd.DataFrame(list(self.mongo.db["tecnicos"].find({"tecnico_id": tecnico_id}, {"tecnico_id": 1, "nome": 1, "especialidade": 1, "email": 1, "telefone": 1, "_id": 0})))

        if external:
            self.mongo.close()

        return dfTecnico
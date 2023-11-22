import pandas as pd
from model.clientes import Cliente
from conexion.mongoQueries import MongoQueries

class ControllerCliente:
    def __init__(self):
        self.mongo = MongoQueries()

    def inserirCliente(self) -> Cliente:

        self.mongo.connect()

        cliente_id = int(input("Informe o ID do novo cliente: "))

        if self.verificaExistenciaCliente(cliente_id):
            nome = input("Nome: ")
            endereco = input("Endereço: ")
            email = input("E-mail: ")
            telefone = input("Telefone: ")

            self.mongo.db["clientes"].insert_one({"cliente_id": cliente_id, "nome": nome, "endereco": endereco, "email": email, "telefone": telefone})

            dfCliente = self.recuperaCliente(cliente_id)

            novoCliente = Cliente(dfCliente.cliente_id.values[0], dfCliente.nome.values[0], dfCliente.endereco.values[0], dfCliente.email.values[0], dfCliente.telefone.values[0])

            print(novoCliente.to_String())
            self.mongo.close()
            return novoCliente
    
        else:
            self.mongo.close()
            print(f"O ID {cliente_id} já pertence a um cliente.")
            return None

    def atualizarCliente(self) -> Cliente:
        self.mongo.connect()

        cliente_id = int(input("Informe o ID do cliente que terá os dados alterados: "))

        if not self.verificaExistenciaCliente(cliente_id):
            novo_nome = input("Novo nome: ")
            novo_endereco = input("Novo endereço: ")
            novo_email = input("Novo e-mail: ")
            novo_telefone = input("Novo telefone: ")

            self.mongo.db["clientes"].update_one({"cliente_id": cliente_id}, {"$set": {"nome": novo_nome, "endereco": novo_endereco, "email": novo_email, "telefone": novo_telefone}})

            dfCliente = self.recuperaCliente(cliente_id)

            clienteAtualizado = Cliente(dfCliente.cliente_id.values[0], dfCliente.nome.values[0], dfCliente.endereco.values[0], dfCliente.email.values[0], dfCliente.telefone.values[0])

            print(clienteAtualizado.to_String())
            self.mongo.close()

            return clienteAtualizado
        else:
            self.mongo.close()
            print(f"O ID {cliente_id} não foi encontrado para ser atualizado.")
            return None

    def excluirCliente(self):
        self.mongo.connect()

        cliente_id = int(input("ID do cliente que deseja excluir: "))

        if not self.verificaExistenciaCliente(cliente_id):
            dfCliente = self.recuperaCliente(cliente_id)

            self.mongo.db["clientes"].delete_one({"cliente_id":cliente_id})

            clienteExcluido = Cliente(dfCliente.cliente_id.values[0], dfCliente.nome.values[0], dfCliente.endereco.values[0], dfCliente.email.values[0], dfCliente.telefone.values[0])
            self.mongo.close()

            print("Cliente removido com sucesso")
            print(clienteExcluido.to_String())
        else:
            self.mongo.close()
            print(f"O ID {cliente_id} não foi encontrado para exclusão.")

    def verificaExistenciaCliente(self, cliente_id: int = None, external:bool=False) -> bool:
        if external:
            self.mongo.connect()
        
        dfCliente = pd.DataFrame(self.mongo.db["clientes"].find({"cliente_id": cliente_id}, {"cliente_id": 1, "nome": 1, "endereco": 1, "email": 1, "telefone": 1, "_id": 0}))
        print(dfCliente)
        if external:
            self.mongo.close()

        return dfCliente.empty
    
    def recuperaCliente(self, cliente_id: int = None, external:bool=False) -> pd.DataFrame:
        if external:
            self.mongo.connect()

        dfCliente = pd.DataFrame(list(self.mongo.db["clientes"].find({"cliente_id": cliente_id}, {"cliente_id": 1, "nome": 1, "endereco": 1, "email": 1, "telefone": 1, "_id":0})))
       
        if external:
            self.mongo.close()

        return dfCliente
    
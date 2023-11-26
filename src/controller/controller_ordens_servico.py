import pandas as pd
from controller.controller_tecnicos import ControllerTecnico
from controller.controller_pecas_utilizadas import ControllerPecasUtilizadas
from reports.relatorios import Relatorio
from model.ordens_servico import OrdemServico
from conexion.mongoQueries import MongoQueries
from model.clientes import Cliente
from model.pecas_utilizadas import PecaUtilizada
from model.tecnicos import Tecnico
from controller.controller_clientes import ControllerCliente


class ControllerOrdemServico:
    def __init__(self):
        self.mongo = MongoQueries()
        self.relatorio = Relatorio()
        self.ctrlCliente = ControllerCliente()
        self.ctrlPecaUtilizada = ControllerPecasUtilizadas()
        self.ctrlTecnico = ControllerTecnico()

    def inserirOrdemServico(self) -> OrdemServico:

        self.mongo.connect()

        self.relatorio.get_relatorioClientes()
        cliente_id = int(input("Informe ID do cliente da Ordem de Serviço: "))
        cliente = self.validaCliente(cliente_id)
        if cliente == None:
            return None
        
        self.relatorio.get_relatorioTecnicos()
        tecnico_id = int(input("Informe o ID do técnico responsável pela OS: "))
        tecnico = self.validaTecnico(tecnico_id)
        if tecnico == None:
            return None
        
        self.relatorio.get_relatorioPecasUtilizadas()
        cod_peca_utilizada = int(input("Informe o código do conjuto de paças utilizadas: "))
        pecaUtilizada = self.validaPecaUtilizada(cod_peca_utilizada)
        if pecaUtilizada == None:
            return None

        ordem_id = int(input("Informe o número da OS: "))

        if self.verificaExistenciaOrdemServico(ordem_id):

            data_abertura = input("Informe a data de abertura da OS (DD/MM/AAAA): ")
            data_conclusao = input("Informe a data de conclusão da OS (DD/MM/AAAA): ")
            status_os = str(input("Informe o status da OS: "))
            custo_total = float(input("Informe o valor total da OS: R$"))

            data = dict(ordem_id=ordem_id, cliente_id=int(cliente.get_cliente_id()), tecnico_id=int(tecnico.get_tecnico_id()), cod_peca_utilizada=int(pecaUtilizada.get_codigo()), data_abertura=data_abertura, data_conclusao=data_conclusao, status_os=status_os, custo_total=custo_total)

            self.mongo.db["ordens_servico"].insert_one(data)

            dfOrdemServico = self.recuperaOrdemServico(ordem_id)

            novaOrdemServico = OrdemServico(dfOrdemServico.ordem_id.values[0], dfOrdemServico.cliente_id.values[0], dfOrdemServico.tecnico_id.values[0], dfOrdemServico.cod_peca_utilizada.values[0], dfOrdemServico.data_abertura.values[0], dfOrdemServico.data_conclusao.values[0], dfOrdemServico.status_os.values[0], dfOrdemServico.custo_total.values[0])

            print(novaOrdemServico.to_string())
            self.mongo.close()
            return novaOrdemServico
        else:
            self.mongo.close()
            print(f"O ID nº {ordem_id}, já foi cadastrada.")
            return None

    def atualizarOrdemServico(self) -> OrdemServico:
        self.mongo.connect()

        ordem_id = int(input("Informe o número da ordem de serviço que será alterada: "))

        if not self.verificaExistenciaOrdemServico(ordem_id):

            self.relatorio.get_relatorioClientes()
            cliente_id = int(input("Digite o ID do cliente: "))
            cliente = self.validaCliente(cliente_id)
            if cliente == None:
                return None

            self.relatorio.get_relatorioTecnicos()
            tecnico_id = int(input("Digite o ID do técnico: "))
            tecnico = self.validaTecnico(tecnico_id)
            if tecnico == None:
                return None
            
            self.relatorio.get_relatorioPecasUtilizadas()
            cod_peca_utilizada = int(input("Digite o código do conjunto de peças utilizadas: "))
            pecaUtilizada = self.validaPecaUtilizada(cod_peca_utilizada)
            if pecaUtilizada == None:
                return None

            data_abertura = input("Informe a nova data de abertura da Ordem de Serviço (DD/MM/AAAA): ")
            data_conclusao = input("Informe a nova data de conclusão da Ordem de Serviço (DD/MM/AAAA): ")
            status_os = input("Informe o status novo da Ordem de Serviço: ")
            novo_custo_total = float(input("Informe o novo custo total da OS: R$"))

            self.mongo.db["ordens_servico"].update_one({"ordem_id": ordem_id},{"$set":{"cliente_id": int(cliente.get_cliente_id()), "tecnico_id": int(tecnico.get_tecnico_id()), "cod_peca_utilizada": int(pecaUtilizada.get_codigo()), "data_abertura": data_abertura, "data_conclusao": data_conclusao, "status_os": status_os, "custo_total": novo_custo_total}})

            dfOrdemServico = self.recuperaOrdemServico(ordem_id)

            ordemServicoAtualizada = OrdemServico(dfOrdemServico.ordem_id.values[0], dfOrdemServico.cliente_id.values[0], dfOrdemServico.tecnico_id.values[0], dfOrdemServico.cod_peca_utilizada.values[0], dfOrdemServico.data_abertura.values[0], dfOrdemServico.data_conclusao.values[0], dfOrdemServico.status_os.values[0], dfOrdemServico.custo_total.values[0])

            print(ordemServicoAtualizada.to_string())
            self.mongo.close()

            return ordemServicoAtualizada
        else:
            self.mongo.close()
            print(f"A ordem de serviço nº, {ordem_id}, não existe. ")
            return None

    def excluirOrdemServico(self) -> OrdemServico:
        self.mongo.connect()

        ordem_id = int(input("Informe o número da ordem de serviço que será excluída: "))

        if not self.verificaExistenciaOrdemServico(ordem_id):

            dfOrdemServico = self.recuperaOrdemServico(ordem_id)
            
            pecaUtilizada = self.validaPecaUtilizada(int(dfOrdemServico['cod_peca_utilizada'].values[0]))
            
            print("Atenção! Caso a Ordem de Serviço possua conjunto de peças atrelada a ela, também serão excluídas!")
            opcaoExcluir = input(f"Tem certeza que deseja excluir a OS nº {ordem_id} (S | N)? ").upper()

            cod_pecaUtilizada = int(input("Confirme o ID do conjunto de peças que será excluído: "))

            if opcaoExcluir == "S":

                ordemServicoExcluida = OrdemServico(dfOrdemServico.ordem_id.values[0], dfOrdemServico.cliente_id.values[0], dfOrdemServico.tecnico_id.values[0], dfOrdemServico.cod_peca_utilizada.values[0], dfOrdemServico.data_abertura.values[0], dfOrdemServico.data_conclusao.values[0], dfOrdemServico.status_os.values[0], dfOrdemServico.custo_total.values[0])

                self.mongo.db["pecas_utilizadas"].delete_one({"codigo": cod_pecaUtilizada})
                print("Peças utilizadas excluídas com sucesso!")

                self.mongo.db["ordens_servico"].delete_one({"ordem_id": ordem_id})
                print("OS removida com sucesso!")

                self.mongo.close()
                
                print(ordemServicoExcluida.to_string())
            
        else:
            self.mongo.close()
            print(f"A ordem de serviço nº, {ordem_id}, não existe. ")
    

    def verificaExistenciaOrdemServico(self, ordem_id: int = None,  external:bool=False) -> bool:
        if external:
            self.mongo.connect()

        dfOrdemServico = pd.DataFrame(self.mongo.db["ordens_servico"].find({"ordem_id": ordem_id}, {"ordem_id": 1, "cliente_id": 1, "tecnico_id": 1, "cod_peca_utilizada": 1, "data_abertura": 1, "data_conclusao": 1, "status_os": 1, "custo_total": 1,"_id": 0}))
        
        if external:
            self.mongo.close()

        return dfOrdemServico.empty
    
    def recuperaOrdemServico(self, ordem_id: int = None, external:bool=False) -> pd.DataFrame:
        if external:
            self.mongo.connect()

        dfOrdemServico = pd.DataFrame(list(self.mongo.db["ordens_servico"].find({"ordem_id": ordem_id}, {"ordem_id": 1, "cliente_id": 1, "tecnico_id": 1, "cod_peca_utilizada": 1, "data_abertura": 1, "data_conclusao": 1, "status_os": 1, "custo_total": 1, "_id": 0})))
        
        if external:
            self.mongo.close()

        return dfOrdemServico
    
    def validaCliente(self, cliente_id: int = None) -> Cliente:

        if self.ctrlCliente.verificaExistenciaCliente(cliente_id, external = True):
            print(f"O cliente {cliente_id} não encontra se na base.")
            return None
        else:

            dfCliente = self.ctrlCliente.recuperaCliente(cliente_id, external=True)

            cliente = Cliente(dfCliente.cliente_id.values[0], dfCliente.nome.values[0], dfCliente.endereco.values[0], dfCliente.email.values[0], dfCliente.telefone.values[0])

            return cliente
    
    def validaTecnico(self, tecnico_id: int = None) -> Tecnico:

        if self.ctrlTecnico.verificaExistenciaTecnico(tecnico_id, external = True):
            print(f"O técnico {tecnico_id} não encontra se na base.")
            return None
        else:
            dfTecnico = self.ctrlTecnico.recuperaTecnico(tecnico_id, external=True)

            tecnico = Tecnico(dfTecnico.tecnico_id.values[0], dfTecnico.nome.values[0], dfTecnico.especialidade.values[0], dfTecnico.telefone.values[0], dfTecnico.valor_os.values[0])

            return tecnico

    def validaPecaUtilizada(self, codigo: int = None) -> PecaUtilizada:

        if self.ctrlPecaUtilizada.verificaExistenciaPecaUtilizada(codigo, external=True):
            print(f"O conjunto de pecas utilizadas não encontra-se na base.")
            return None
        
        else:

            dfPecaUtilizada = self.ctrlPecaUtilizada.recuperaPecaUtilizada(codigo, external=True)

            pecaUtilizada = PecaUtilizada(dfPecaUtilizada.codigo.values[0], dfPecaUtilizada.peca_id.values[0], dfPecaUtilizada.quant_utilizada.values[0])

            return pecaUtilizada
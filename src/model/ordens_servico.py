from model.pecas_utilizadas import PecaUtilizada
from model.clientes import Cliente
from model.tecnicos import Tecnico

class OrdemServico:
    def __init__(self,
                 ordem_id: int = None,
                 cliente_id: Cliente = None,
                 tecnico_id: Tecnico = None,
                 codigo_peca_utilizada: PecaUtilizada = None,
                 data_abertura: str = None,
                 data_conclusao: str = None,
                 status_os: str = None,
                 solucao: str = None,
                 custo_total: float = None):
        self.set_ordem_id(ordem_id)
        self.set_cliente_id(cliente_id)
        self.set_tecnico_id(tecnico_id)
        self.set_codigo_peca_utilizada(codigo_peca_utilizada)
        self.set_data_abertura(data_abertura)
        self.set_data_conclusao(data_conclusao)
        self.set_statusOs(status_os)
        self.set_solucao(solucao)
        self.set_custo_total(custo_total)

    def set_ordem_id(self, ordem_id: int):
        self.ordem_id = ordem_id

    def set_cliente_id(self, cliente_id: Cliente):
        self.cliente_id = cliente_id

    def set_tecnico_id(self, tecnico_id: Tecnico):
        self.tecnico_id = tecnico_id

    def set_codigo_peca_utilizada(self, codigo_peca_utilizada: PecaUtilizada):
        self.codigo_peca_utilizada = codigo_peca_utilizada

    def set_data_abertura(self, data_abertura: str):
        self.data_abertura = data_abertura

    def set_data_conclusao(self, data_conclusao: str):
        self.data_conclusao = data_conclusao

    def set_statusOs(self, status_os: str):
        self.status_os = status_os

    def set_solucao(self, solucao: str):
        self.solucao = solucao

    def set_custo_total(self, custo_total: float):
        self.custo_total = custo_total

    def get_ordem_id(self) -> int:
        return self.ordem_id

    def get_cliente_id(self) -> Cliente:
        return self.cliente_id

    def get_tecnico_id(self) -> Tecnico:
        return self.tecnico_id
    
    def get_codigo_peca_utilizada(self) -> PecaUtilizada:
        return self.codigo_peca_utilizada

    def get_data_abertura(self) -> str:
        return self.data_abertura

    def get_data_conclusao(self) -> str:
        return self.data_conclusao

    def get_statusOs(self) -> str:
        return self.status_os

    def get_solucao(self) -> str:
        return self.solucao

    def get_custo_total(self) -> float:
        return self.custo_total

    def to_string(self) -> str:
        return f"Ordem de Serviço ID: {self.ordem_id} | Cliente ID: {self.cliente_id} | Tecnico ID: {self.tecnico_id} | Código peça utilizada: {self.codigo_peca_utilizada} | Data de abertura: {self.data_abertura}| Data de conclusão: {self.data_conclusao} | Status OS: {self.status_os} | Solução: {self.solucao} | Custo total: {self.custo_total} "
class Tecnico:
    def __init__(self,
                tecnico_id: int = None,
                nome: str = None,
                especialidade: str = None,
                telefone: str = None,
                valor_os: float = None):
        self.set_tecnico_id(tecnico_id)
        self.set_nome(nome)
        self.set_especialidade(especialidade)
        self.set_telefone(telefone)
        self.set_valor_os(valor_os)

    def set_tecnico_id(self, tecnico_id: int):
        self.tecnico_id = tecnico_id

    def set_nome(self, nome: str):
        self.nome = nome

    def set_especialidade(self, especialidade: str):
        self.especialidade = especialidade

    def set_telefone(self, telefone: str):
        self.telefone = telefone

    def set_valor_os(self, valor_os: float):
        self.valor_os = valor_os

    def get_tecnico_id(self) -> int:
        return self.tecnico_id

    def get_nome(self) -> str:
        return self.nome

    def get_especialidade(self) -> str:
        return self.especialidade

    def get_telefone(self) -> str:
        return self.telefone
    
    def get_valor_os(self) -> float:
        return self.valor_os

    def to_String(self) -> str:
        return f"Tecnico ID: {self.tecnico_id} | Nome: {self.nome} | Especialidade: {self.especialidade} " \
               f"| Telefone: {self.telefone} | Valor cobrado por OS: {self.valor_os}"
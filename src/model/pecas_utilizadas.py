from model.pecas import Peca

class PecaUtilizada:
    def __init__(self,
                 codigo: int = None,
                 peca_id: Peca = None,
                 quant_utilizada: int = None):
        self.set_codigo(codigo)
        self.set_peca_id(peca_id)
        self.set_quant_utilizada(quant_utilizada)

    def set_codigo(self, codigo: int):
        self.codigo = codigo

    def set_peca_id(self, peca_id: Peca):
        self.peca_id = peca_id

    def set_quant_utilizada(self, quant_utilizada: str):
        self.quant_utilizada = quant_utilizada

    def get_codigo(self) -> int:
        return self.codigo

    def get_peca_id(self) -> Peca:
        return self.peca_id

    def get_quant_utilizada(self) -> int:
        return self.quant_utilizada

    def to_String(self) -> str:
        return f"Codigo: {self.codigo} | Peca ID: {self.peca_id} | Quantidade Utilizada: {self.quant_utilizada}"
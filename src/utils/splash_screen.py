from utils import config

class SplashScreen:

    def __init__(self):
        self.created_by = "Artur Hollanda, Bernardo Rocha, Pablo Moura e Olívia Noronha"
        self.professor = "Prof. M.Sc. Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2023/2"

    def get_documentsCount(sel, collection_name):
        df = config.queryCount(collection_name=collection_name)
        return df[f"total_{collection_name}"].values[0]
    
    def get_updatedScreen(self):
        return f"""
        ########################################################
        #            CADASTRO DE ORDENS DE SERVIÇO    
        #                                                         
        #  TOTAL DE REGISTROS:                                    
        #      1 - CLIENTES:          {str(self.get_documentsCount(collection_name="clientes")).rjust(5)}
        #      2 - TÉCNICOS:          {str(self.get_documentsCount(collection_name="tecnico")).rjust(5)}
        #      3 - PEÇAS:             {str(self.get_documentsCount(collection_name="peca")).rjust(5)}
        #      4 - PEÇAS UTILIZADAS:  {str(self.get_documentsCount(collection_name="pecas_utilizadas")).rjust(5)}
        #      5 - ORDENS DE SERVIÇO: {str(self.get_documentsCount(collection_name="ordem_servico")).rjust(5)}
        #
        #  CRIADO POR: {self.created_by}
        #
        #  PROFESSOR:  {self.professor}
        #
        #  DISCIPLINA: {self.disciplina}
        #              {self.semestre}
        ########################################################
        """
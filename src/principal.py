from controller.controller_ordens_servico import ControllerOrdemServico
from controller.controller_tecnicos import ControllerTecnico
from controller.controller_pecas_utilizadas import ControllerPecasUtilizadas
from controller.controller_pecas import ControllerPeca
from reports.relatorios import Relatorio
from controller.controller_clientes import ControllerCliente
from utils import config
from utils.splash_screen import SplashScreen


telaInicial = SplashScreen()
ctrlClientes = ControllerCliente()
ctrlPecas = ControllerPeca()
ctrlTecnicos = ControllerTecnico()
ctrlOrdensServico = ControllerOrdemServico()
ctrlPecasUtilizadas = ControllerPecasUtilizadas()
relatorios = Relatorio()

def reports(opcao_relatorio:int=0):

    if opcao_relatorio == 1:
        relatorios.get_relatorioClientes()
    elif opcao_relatorio == 2:
        relatorios.get_relatorioTecnicos()
    elif opcao_relatorio == 3:
        relatorios.get_relatorioPecas()
    elif opcao_relatorio == 4:
        relatorios.get_relatorioPecasUtilizadas()
    elif opcao_relatorio == 5:
        relatorios.get_relatorioOsConsolidado()
               
    

def inserir(opcao_inserir:int=0):

    if opcao_inserir == 1:                               
        novoCliente = ctrlClientes.inserirCliente()
    elif opcao_inserir == 2:
        novoTecnico = ctrlTecnicos.inserirTecnico()
    elif opcao_inserir == 3:
        novaPeca = ctrlPecas.inserirPeca()
    elif opcao_inserir == 4:
        novaPecaUtilizda = ctrlPecasUtilizadas.cadastrarPecaUtilizada()
    elif opcao_inserir == 5:
        novaOs = ctrlOrdensServico.inserirOrdemServico()
    

def atualizar(opcao_atualizar:int=0):

    if opcao_atualizar == 1:
        relatorios.get_relatorioClientes()
        clienteAtualizado = ctrlClientes.atualizarCliente()
    elif opcao_atualizar == 2:
        relatorios.get_relatorioTecnicos()
        tecnicoAtualizado = ctrlTecnicos.atualizarTecnico()
    elif opcao_atualizar == 3:
        relatorios.get_relatorioPecas()
        pecaAtualizada = ctrlPecas.atualizarPeca()
    elif opcao_atualizar == 4:
        relatorios.get_relatorioPecasUtilizadas()
        pecaUtilizadaAtualizada = ctrlPecasUtilizadas.atualizarPecaUtilizada()
    elif opcao_atualizar == 5:
        relatorios.get_relatorioOsConsolidado()
        ordemServicoAtualizada = ctrlOrdensServico.atualizarOrdemServico()
    

def excluir(opcao_excluir:int=0):

    if opcao_excluir == 1:
        relatorios.get_relatorioClientes()
        ctrlClientes.excluirCliente()
    elif opcao_excluir == 2:
        relatorios.get_relatorioTecnicos()
        ctrlTecnicos.excluirTecnico()
    elif opcao_excluir == 3:
        relatorios.get_relatorioPecas()
        ctrlPecas.excluirPeca()
    elif opcao_excluir == 4:
        relatorios.get_relatorioPecasUtilizadas()
        ctrlPecasUtilizadas.excluirPecasUtilizadas()
    elif opcao_excluir == 5:
        relatorios.get_relatorioOsConsolidado()
        ctrlOrdensServico.excluirOrdemServico()
    

def run():
    print(telaInicial.get_updatedScreen())
    config.clear_console()

    while True:
        print(config.MENU_PRINCIPAL)
        opcao = int(input("Escolha uma opção [1-5]: "))
        config.clear_console(1)
        
        if opcao == 1: # Relatórios
            
            print(config.MENU_RELATORIOS)
            opcao_relatorio = int(input("Escolha uma opção [1-5]: "))
            config.clear_console(1)

            reports(opcao_relatorio)

            config.clear_console(1)

        elif opcao == 2: # Inserir Novos Registros
            
            escolha = "SIM"
            while(escolha=="SIM"):
               print(config.MENU_ENTIDADES)
               opcao_inserir = int(input("Escolha uma opção [1-5]: "))
               config.clear_console(1)

               inserir(opcao_inserir=opcao_inserir)

               escolha = input("Deseja continuar inserindo registros (SIM | NAO)? ").upper()
            
            
            config.clear_console()
            print(telaInicial.get_updatedScreen())
            config.clear_console()

        elif opcao == 3: # Atualizar Registros
            escolha = "SIM"
            while(escolha=="SIM"):

                print(config.MENU_ENTIDADES)
                opcao_atualizar = int(input("Escolha uma opção [1-5]: "))
                config.clear_console(1)

                atualizar(opcao_atualizar=opcao_atualizar)

                escolha = input("Deseja continuar atualizando registros (SIM | NAO)? ").upper()

            config.clear_console()

        elif opcao == 4: # Excluir registros

            escolha = "SIM"

            while(escolha=="SIM"):
               print(config.MENU_ENTIDADES)
               opcao_excluir = int(input("Escolha uma opção [1-5]: "))
               config.clear_console(1)

               excluir(opcao_excluir=opcao_excluir)

               escolha = input("Deseja continuar excluindo registros (SIM | NAO)? ").upper()

            config.clear_console()
            print(telaInicial.get_updatedScreen())
            config.clear_console()

        elif opcao == 5: # Sair

            print(telaInicial.get_updatedScreen())
            config.clear_console()
            print("Obrigado por utilizar o nosso sistema.")
            exit(0)

        else:
            print("Opção incorreta.")
            exit(1)

if __name__ == "__main__":
   run()
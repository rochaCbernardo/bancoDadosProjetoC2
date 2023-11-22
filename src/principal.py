from controller.controller_pecas import ControllerPeca
from reports.relatorios import Relatorio
from controller.controller_clientes import ControllerCliente
from utils import config
from utils.splash_screen import SplashScreen


telaInicial = SplashScreen()
ctrlClientes = ControllerCliente()
ctrlPecas = ControllerPeca()
relatorios = Relatorio()

def reports(opcao_relatorio:int=0):

    if opcao_relatorio == 1:
        relatorios.get_relatorioClientes()
    elif opcao_relatorio ==3:
        relatorios.get_relatorioPecas()
               
    

def inserir(opcao_inserir:int=0):

    if opcao_inserir == 1:                               
        novoCliente = ctrlClientes.inserirCliente()
    elif opcao_inserir == 3:
        novaPeca = ctrlPecas.inserirPeca()
    

def atualizar(opcao_atualizar:int=0):

    if opcao_atualizar == 1:
        relatorios.get_relatorioClientes()
        clienteAtualizado = ctrlClientes.atualizarCliente()
    elif opcao_atualizar == 3:
        relatorios.get_relatorioPecas()
        pecaAtualizada = ctrlPecas.atualizarPeca()
    

def excluir(opcao_excluir:int=0):

    if opcao_excluir == 1:
        relatorios.get_relatorioClientes()
        ctrlClientes.excluirCliente()
    elif opcao_excluir == 3:
        relatorios.get_relatorioPecas()
        ctrlPecas.excluirPeca()
    

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

               escolha = input("Deseja continuar inserindo registros? ").upper()
            
            
            config.clear_console()
            print(telaInicial.get_updatedScreen())
            config.clear_console()

        elif opcao == 3: # Atualizar Registros

            print(config.MENU_ENTIDADES)
            opcao_atualizar = int(input("Escolha uma opção [1-5]: "))
            config.clear_console(1)

            atualizar(opcao_atualizar=opcao_atualizar)

            config.clear_console()

        elif opcao == 4: # Excluir registros

            escolha = "SIM"

            while(escolha=="SIM"):
               print(config.MENU_ENTIDADES)
               opcao_excluir = int(input("Escolha uma opção [1-5]: "))
               config.clear_console(1)

               excluir(opcao_excluir=opcao_excluir)

               escolha = input("Deseja continuar excluindo registros? ").upper()

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
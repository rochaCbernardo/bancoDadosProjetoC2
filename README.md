# bancoDadosProjetoC3
## Sistema de Gestão de Ordens de serviço

Esse sistema é composto por um conjunto de tabelas que representam ordens de serviços geradas após algum tipo de manutenção.

O sistema exige que as tabelas existam, então basta executar o script Python a seguir para criação das tabelas e preenchimento de dados de exemplos:
```shell
~$ python createCollectionsAndData.py
```
Para executar o sistema basta executar o script Python a seguir:
```shell
~$ python principal.py
```
## Organização
- [diagramas](diagramas): Nesse diretório está o [diagrama relacional](diagramas/Diagrama_BD_Trabalho.pdf) do sistema.
    * O sistema possuí 5 entidades, sendo elas: clientes, tecnico, ordem_servico, pecas e pecas_utilizadas.
- [src](src): Nesse diretório estão os scripts do sistema
    * [conexion](src/conexion): Nesse repositório encontra-se o módulo de conexão com o banco de dados Mongo. Esses módulo do Mongo apenas realiza a conexão, os métodos CRUD e de recuperação de dados são implementados diretamente nos objetos controladores (Controllers) e no objeto de Relatório (reports).
    * [controller](src/controller): Nesse diretório encontram-se as classes controladoras, responsáveis por realizar inserção, alteração e exclusão dos registros das tabelas.
    * [model](src/model): Nesse diretório encontram-se as classes das entidades descritas no diagrama relacional.
    * [reports](src/reports): Nesse diretório encontra-se a classe responsável por gerar todos os relatórios do sistema.
    * [utils](src/utils): Nesse diretório encontram-se scripts de configuração e automatização da tela de informações iniciais.
create_collections_and_data.py: Script responsável por criar as tabelas e registros fictícios. Esse script deve ser executado antes do script principal.py para gerar as tabelas, caso não execute os scripts diretamente no SQL Developer ou em alguma outra IDE de acesso ao Banco de Dados.
principal.py: Script responsável por ser a interface entre o usuário e os módulos de acesso ao Banco de Dados. Deve ser executado após a criação das tabelas.
diagrams: Nesse diretório está o diagrama de banco de dados e o diagrama relacional(lógico) do sistema.
O sistema possui cinco entidades: CLIENTE, ORDEM_SERVICO, PECA_UTILIZADA, PECA e TECNICO


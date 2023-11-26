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
      - Exemplo CRUD, controller_clientes:
        ```python
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
        ```
     - Exemplo CRUD, controller_pecas_utilizadas:
       ```python
       def excluirPecasUtilizadas(self) -> PecaUtilizada:
        self.mongo.connect()

        codigo = int(input("Informe o do conjuto de peças utilizadas que será excluído: "))

        if not self.verificaExistenciaPecaUtilizada(codigo):
            dfPecaUtilizada = self.recuperaPecaUtilizada(codigo)
            peca = self.validaPeca(int(dfPecaUtilizada.peca_id.values[0]))

            opcaoExcluir = input(f"Tem certeza que deseja excluir o conjunto de peças ID {codigo}? (S |N) ").upper()
            if opcaoExcluir == "S":
                self.mongo.db["pecas_utilizadas"].delete_one({"codigo": codigo})
                pecaUtilizadaExcluida = PecaUtilizada(dfPecaUtilizada.codigo.values[0], dfPecaUtilizada.peca_id.values[0], dfPecaUtilizada.quant_utilizada.values[0])
                self.mongo.close()

                print("Conjunto removido com sucesso!")
                print(pecaUtilizadaExcluida.to_String())
        else:
            self.mongo.close()
            print(f"O ID {codigo} não existe.")
       ```
    * [model](src/model): Nesse diretório encontram-se as classes das entidades descritas no diagrama relacional.
    * [reports](src/reports): Nesse diretório encontra-se a classe responsável por gerar todos os relatórios do sistema.
         - Exemplos de relatórios:
           ```python
           def get_relatorioClientes(self):

           mongo = MongoQueries()
           mongo.connect()

           query_result = mongo.db["clientes"].find({}, 
                                                 {"cliente_id": 1, 
                                                  "nome": 1,
                                                  "endereco": 1,
                                                  "email": 1,
                                                  "telefone": 1, 
                                                  "_id": 0
                                                 }).sort("nome", ASCENDING)
           dfCliente = pd.DataFrame(list(query_result))
           # Fecha a conexão com o mongo
           mongo.close()
           # Exibe o resultado
           print(dfCliente)
           input("Pressione Enter para Sair do Relatório de Clientes..")
           ```

           ```python
           def get_relatorioPecasUtilizadas(self):
           mongo = MongoQueries()
           mongo.connect()

           query_result = mongo.db["pecas_utilizadas"].aggregate([{
                                                                '$lookup':{'from': "pecas",
                                                                           'localField': "peca_id",'foreignField': "peca_id",'as': "peca_id"
                                                                           }
                                                                           },
                                                                           {
                                                                        '$unwind': {'path': '$peca_id'}
                                                                            },
                                                                           {
                                                                               '$project':
                                                                               {
                                                                               'codigo': 1,
                                                                               'peca_id': '$peca_id.peca_id',
                                                                               'nome': '$peca_id.nome',
                                                                               'valor_peca': '$peca_id.preco_uni',
                                                                               'quant_utilizada': 1,
                                                                               'valor_total_pecas': {'$multiply':["$quant_utilizada", "$peca_id.preco_uni"]},
                                                                               '_id': 0
                                                                               }
                                                                            }])
           dfPecaUtilizada = pd.DataFrame(list(query_result))
           mongo.close()

           print(dfPecaUtilizada[["codigo", "peca_id", "nome", "valor_peca", "quant_utilizada", "valor_total_pecas"]])
           input("Pressione Enter para Sair do Relatório de Peças Utilizadas..")   
           ```
    * [utils](src/utils): Nesse diretório encontram-se scripts de configuração e automatização da tela de informações iniciais.
    * [createCollections.py](src/createCollections.py): Script responsável por criar as tabelas e registros fictícios. Esse script deve ser executado antes do script principal.py para gerar as tabelas, caso não execute os scripts diretamente no SQL Developer ou em alguma outra IDE de acesso ao Banco de Dados.
    * [principal.py](src/principal.py): Script responsável por ser a interface entre o usuário e os módulos de acesso ao Banco de Dados. Deve ser executado após a criação das tabelas.

### Bibliotecas Utilizadas
- [requirements.txt](src/requirements.txt): `pip install -r requirements.txt`


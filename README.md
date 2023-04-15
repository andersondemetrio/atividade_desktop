# atividade_desktop
Aplicativo de bloco de notas
Crie um aplicativo de bloco de notas em Python usando PySide6 e SQLite.
Requisitos funcionais do aplicativo:
-O aplicativo deve permitir ao usuário criar, ler, atualizar e excluir notas.
-As notas devem ser salvas em um banco de dados SQLite.
-As notas devem ter campos para ID (auto incrementável), nome da nota, data da nota (deve ser
capturada na hora do salvamento da nota) e texto da nota.
-As notas devem ser exibidas em uma QTableWidget, onde o usuário pode clicar duas vezes em
uma linha para editar a nota correspondente.
-Ao clicar duas vezes em uma linha, os campos devem ser preenchidos com as informações
da nota, incluindo o ID, que deve ser desativado para edição.
-A tabela de notas deve ser apenas para visualização, sem a possibilidade de seleção ou
edição direta.
Regras de negócio:
-Criar nota: O usuário pode criar uma nova nota, preenchendo o nome da nota e o texto da nota e
clicando em um botão de salvar.
-Ler nota: O usuário pode visualizar as notas existentes na tabela, que mostra o ID da nota, o nome
da nota e a data da nota.
-Editar nota: O usuário pode clicar duas vezes em uma linha da tabela para editar uma nota
existente. Os campos devem ser preenchidos com as informações da nota correspondente e o ID deve ser
desativado para edição. O texto do botão Salvar deve ser alterado para Atualizado. Deve ser mostrado o
botão remover. O usuário pode editar o nome e o texto da nota e clicar em um botão de salvar para
atualizar a nota.
-Excluir nota: O usuário pode excluir uma nota existente selecionando-a na tabela e clicando em um
botão de excluir.
Ao implementar o aplicativo, certifique-se de usar as boas práticas de programação, incluindo
modularidade, encapsulamento e tratamento adequado de erros e arquitetura MVC.
Protótipo:

title: [PT] Construindo uma ferramenta para criação de notas rápidas
date: 2021-01-20 01:05
author: diego
tags: ferramental, python, recriação, dontpad
slug: construindo-uma-ferramenta-para-criacao-de-notas-rapidas
og_image: assets/images/code.jpg

Em um ambiente de desenvolvimento de software, as pessoas que compõem um time/projeto/*squad* tendem a compartilhar dados entre si a todo momento. *Logs* de aplicação, trechos de código e macetes muitas vezes extrapolam o limite de caracteres da ferramenta de comunicação, fazendo com que surja a necessidade de colar essa informação em uma ferramenta externa.

Na empresa onde trabalho, por exemplo, usamos com frequência o site **[dontpad.com](http://dontpad.com/)**. **Dontpad** é uma aplicação que possibilita a criação rápida de notas a partir de um recurso definido pelo usuário. Uma sequência de caracteres qualquer após a URL `http://dontpad.com`, já torna um identificador para o conteúdo do seu texto. O Dontpad é extramente rápido e eficiente, porém observei alguns contras:

-   Nenhuma privacidade e segurança. Qualquer pessoa que tiver a URL, da sua nota, pode visualizar o conteúdo.
-   Nenhuma consistência. Qualquer pessoa que tiver a URL também pode alterar o conteúdo, e até mesmo apagá-lo.
-   Não é possível saber quem modificou um arquivo. Tudo é anônimo.

![Exemplo de uso do Dontpad](/assets/images/dontpad-hello.gif)*Criando uma nota pelo Dontpad.*

Algo que está se tornando cada vez mais comum no aprendizado e exercício do desenvolvimento de software, nos dias atuais, é a criação de projetos que simulam alguma plataforma de sucesso. Recriar, mesmo que de maneira simplória, réplicas como do UX do Instagram, backend do Uber, arquitetura da Netflix, nos induzem a refletir sobre técnicas que podem usadas nesses cases.

Dado isso, uni todas as características ruíns do Dontpad, joguei num balde, e me desafiei a refazê-lo com algumas melhorias. Apesar de ser um serviço bem respaldado e com muitos acessos, a ideia por trás do Dontpad não é complexa. O grau de dificuldade inclusive foi maior no conjunto de funcionalidades que adicionei como diferenciais:

-   A URL de uma nota é *hash* (ex: https:///EreQR5z).
-   Possibilidade de criar conta para guardar notas.
-   Possibilidade de privar notas para o usuário.
-   Capacidade de bloquear a alteração do conteúdo de uma nota.
-   Capacidade de saber quando uma nota foi criada e a última vez que foi alterada.
-   Capacidade de saber quem viu uma nota.
-   Pesquisa de notas por fragmento de conteúdo.
-   Adaptação para dispositivos móveis (responsivo).
-   Modo escuro (*dark theme*).

Atualmente, tenho voltado os meus esforços para aprendizado e aperfeiçoamento da linguagem Java. Mas, para esse projeto, preferi usar a stack formada pela linguagem **Python** e o framework **Django**. Considero como uma das maiores vantagens de usar essa tecnologia, a rapidez em que é possível levantar uma aplicação com várias baterias embutidas, tais como: sistema de autenticação e migração de banco de dados. Como é de costume em projetos que envolvem algum tipo de interface gráfica, começo sempre pelo *wireframe*. A imagem abaixo são as ideias iniciais das telas.

![Daptnod wireframe](/assets/images/daptnot-wireframe.jpeg)*Wireframe desenhado para guiar a construção das telas.*

Como até aquele momento às novas funcionalidades da aplicação estavam definidas, já se sabia quais campos eram necessários para formular o domínio principal do sistema: **as notas**. A tabela denomida para este fim, `notes_note`, se relaciona com a tabela de usuários, `auth_user`, em dois campos: `created_by_id` e `updated_by_id`. Uma das funcionalidades consistia em saber quais pessoas visualizaram uma nota, para isso foi preciso fazer uma relação *ManyToMany* através da tabela `notes-note-viewers`, como sugere a imagem a seguir.

![Daptnod modelagem](/assets/images/modelagem-daptnod.jpeg)*Relação entre os modelos de Notas e Usuários.*

Depois de criado o modelo, o resto do tempo foi investido para construir o *frontend* e otimizar consultas. Destaco aqui uma ferramenta que ajuda bastante nesse último ponto, que é o [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/). Essa dependência, quando configurada e habilitada, possibilita fazer um "raio X" do que acontece quando uma requisição chega até o servidor. Alguns exemplos de otimizações que foram feitas usando o ORM que o próprio Django fornece, foram:

```python
# Antes 
note = Note() 
...
note.views_number = note.views_number + 1
note.save() 

# Depois 
Note.objects.filter(pk=note.pk).update(
    views_number=note.views_number + 1
) 
```

```python

# Antes
note = Note()
...
note.updated_at = timezone.now()
note.updated_by = None
note.content = request.POST.get('content')
note.save() 

# Depois
Note.objects.filter(pk=note.pk).update(
    updated_at = timezone.now(),
    updated_by = None,
    content = request.POST.get('content')
)

```

As telas foram feitas com o framework CSS [Bulma](https://bulma.io/). A intenção foi deixá-las o mais simples possível, sem truques nem efeitos. Mesmo focando no básico, sentia falta do "modo escuro" que não existia no Dontpad. Não é tão simples fazer isso com o Bulma, mas encontrei uma extensão que facilitou o desenvolvimento desse recurso: [bulma-prefers-dark](https://github.com/jloh/bulma-prefers-dark). Ao final da construção, a navegação ficou assim:

![Daptnod modelagem](/assets/images/tuor-daptnod.gif)*Tuor pelo Daptnod.*

Apesar de ser algo simples, este foi um dos projetos que mais gostei de fazer por ser muito útil. O tempo de desenvolvimento da aplicação foi de aproximadamente duas semanas. Oficializei uma primeira versão da ferramenta e a batizei como **DAPTNOD**. O projeto está no GitHub através deste [link](https://github.com/diegofsousa/daptnod). Também subi uma versão de produção que pode ser acessada em <https://daptnod.herokuapp.com/>.

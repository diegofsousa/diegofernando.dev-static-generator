title: [PT] Adicionando Eclipse Spring Tools 4 ao lançador do Ubuntu
date: 2020-05-16 23:54
author: diego
tags: programação, java, spring, ide, eclipse
slug: adicionando-eclipse-spring-tools-4-lancador-ubuntu
og_image: assets/images/tool.jpg

Uma das mais famosas IDE's (_Integrated Development Environment_) para a criação de programas em Java é o **Eclipse**. O seu uso simples torna o desenvolvimento bastante produtivo. Já o **Spring Tools 4** (ou simplemente **STS**) é basicamente um _plugin_ criado exclusivamente para o framework _web_ Java **Spring** que tem suporte para o ambientes **Eclipse**, **Visual Studio Code** e **Theia**. 

Mesmo sendo um _plugin_, ao efetuar o _download_ do STS, estamos também baixando o Eclipse, pois o STS funciona como uma extensão dessa IDE. A maneira mais básica de começar a utilizar o STS no ambiente Linux é baixá-la diretamente do [site oficial](https://spring.io/tools) e rodar o arquivo executável. Veja o GIF a seguir.

![Inicialização manual STS](/assets/images/sts-manual.gif)*Inicialização manual do STS.*

Essa tarefa começa a ficar incômoda quando toda vez temos que abrir um diretório e ter que rodar. Os perfeccionistas (como eu) acabam achando essa uma abordagem ruim. Nos próximos passos iremos ver como inserir o _software_ no lançador (_launch_) e ainda como configurar para deixá-lo nos favoritos.

## Mão na massa

> ⚠️ _Disclaimer_: Esse procedimento foi testado com o STS na versão `4.6.1` e o Ubuntu na versão `18.04`.

O primeiro passo é mover a pasta extraída do download para o diretório `/opt`:

```shell
sudo mv <diretorio-sts> /opt
```
Certo, vamos então criar um ícone para o lançador. Todos o ícones de _softwares_ instalados no Ubuntu 18.04 ficam em `/usr/share/applications`. Entre nesse diretório e crie um arquivo `"sts.desktop"` com o seguinte conteúdo:

Arquivo `"sts.desktop"`
```shell
[Desktop Entry]
Type=Application
Name=sts
Comment=Spring Tool Suite
Icon=/opt/<diretorio-sts>/icon.xpm
Exec=/opt/<diretorio-sts>/SpringToolSuite4
Terminal=false
Categories=Development;IDE;Java;
```
Substitua `<diretorio-sts>` pela pasta que você nomeou dentro de `/opt`.

Se tudo tiver corrido bem, já podemos encontrar o STS entre os ícones do lançador. 

Esse processo funciona até o momento em que adicionamos o ícone a barra de favoritos. Até conseguimos inseri-lo na barra, mas ao executar notamos que ele duplica o ícone:

![Inicialização com ícone duplicado](/assets/images/sts-duplicated.jpeg)*Inicialização com ícone duplicado.*

Para corrigir esse _bug_, voltamos ao diretório `/usr/share/applications` para editar o nosso 
`"sts.desktop"`. Iremos adicionar a linha `StartupWMClass=Spring Tool Suite 4` ao arquivo. O valor **Spring Tool Suite 4** deve ser exatamente igual ao nome do _software_. Felizmente existe uma forma de assegurar isso com o comando `xprop WM_CLASS`:

![Adquirindo nome absoluto do software](/assets/images/sts-get-name-software.gif)*Adquirindo nome absoluto do software.*

Dessa forma, o arquivo final `"sts.desktop"`  fica:
```shell
[Desktop Entry]
Type=Application
Name=sts
Comment=Spring Tool Suite
Icon=/opt/<pasta-sts>/icon.xpm
Exec=/opt/<pasta-sts>/SpringToolSuite4
Terminal=false
Categories=Development;IDE;Java;
StartupWMClass=Spring Tool Suite 4
```

Ao fazer isso, adicione novamente o ícone aos favoritos e confirme se funcionou. O comportamento deve ser similar ao do exemplo abaixo:

![STS disponível no lançador](/assets/images/sts-on-launch.gif)*STS disponível no lançador.*

Comente se funcionou (ou não) aqui em baixo. :)
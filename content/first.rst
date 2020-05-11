[PT] Configurando rotas estáticas em uma rede
#############################################
:date: 2019-09-26 00:45
:author: diego
:tags: laboratório, cisco
:slug: configurando-rotas-estaticas-em-uma-rede

Imagine o seguinte cenário: temos uma tarefas de criar uma comunicação entre duas redes diferentes. Em cada rede existe um roteador na borda e, claramente, devemos implantar um outro roteador que possa interconectar essas duas redes. As redes são:


router0: 10.10.0.0 /16 /
router2: 10.20.0.0 /16


Iremos então adicionar um terceiro router e iremos chamá-lo de "router1". Ao efetuar a conexão, com todas as configurações DTE/DCE nas duas pontas devidamente configuradas, ainda obtemos erro de PING de uma ponta a outra. Isso acontece pelo fato de não existir nenhuma rota de "router0" para "router2" e vice-versa.

Entramos no nosso "router0" em modo config e criamos uma rota estática para "router2" com o comando "iproute":

ip route 10.20.0.0 255.255.0.0 10.10.0.1

Neste contexto o primeiro endereço IP refere-se a rede que se deseja alcançar e o segundo IP é a mascara específica. O último endereço indica o meio em que vamos alcançar nossa rede desejada, ou seja o IP da inteface conectada ao "router1". Nossa topologia segue então a seguinte figura:

|Image|

Não devemos esquecer de efetuar o mesmo procedimento no "router2":

ip route 10.10.0.0 255.255.0.0 10.10.0.2

Observe que neste caso alteramos o IP do nosso roteador do meio, pois este é o IP que nosso "router2" se conecta ao "router1". Efetuando o comando PING de uma ponta a outra, podemos verificar que agora temos conexão.

.. |Image| image:: /assets/images/esquematico-rota-estatica.jpeg
   :target: /assets/images/esquematico-rota-estatica.jpeg
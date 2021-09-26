# Animação Facial

O trabalho deste repositório, faz parte da tese de doutorado _Modelagem e síntese de aspectos faciais da Língua Brasileira de Sinais para avatares sinalizantes_ desenvolvido por Ackley Dias Will e orientado pelo prof. Dr. José Mario De Martino da Faculdade de Engenharia Elétrica e de Computação (FEEC) da Universidade Estadual de Campinas (UNICAMP). O sistema tem como objetivo validar a metodologia de criação de animações faciais para acompanhar as animações corporais apresentada no trabalho da tese.



# 1. Sistema Piloto

O sistema piloto aqui descrito foi escrito na linguagem de programação Python. O arquivo CreateAnimation.py apresenta os códigos do sistema. Caso necessário, os parâmetros envolvendo os caminhos dos arquivos de sentenças e regras e caminho do repositório podem ser alterados na seção do código demarcada como _Parâmetros iniciais_. Os códigos foram comentados para melhor entendimento das funcionalidades. A seguir sao apresentados os arquivos, configurações e parâmetros que envolvem a execução do sistema piloto.


## 1.1.  Arquivos de parâmetros do sistema

Como parâmetro do sistema são exigidos: o arquivo de sentenças e anotações, o arquivo de regras e o caminho do repositório das expressões faciais. 


_**Arquivo: sentenças.txt**_

O arquivo sentencas.txt contém as sentenças em glosas e a descrição dos instantes de início de cada transição e sinal sinalizado assim como o instante de término da animação corporal. Abaixo está listado o conteúdo do arquivo com duas sentenças e suas anotações:

_CASAS HOMEM EL@ VENDER VAI?_

_T360,S440,T535,S573,T620,S643,T691,S726,T766,S815,T914,E1023_

_HOMEM CONSTRUIR CASAS COMO?_

_T488,S540,T593,S630,T695,S740,T805,S835,T948,E1038_


_**Arquivo:  regras.txt**_

Neste arquivo são descritas as regras associadas aos sinais da Libras. Em cada linha é apresentado o sinal e sua regra associada. Abaixo está listado um trecho do conteúdo do arquivo regras.txt:

_ONDE? B1_

_QUANDO? B1_

_COMO? B1A1_

_POR-QUE? B1A1_


_**Repositório de expressões faciais**_

Os trechos de animações de expressões faciais são salvos em arquivos independentes em um diretório que representa o repositório de expressões faciais. O nome de cada arquivo é composto pelo tipo da expressão facial seguido por um número inteiro sequencial. Os diferentes tipos de expressões faciais utilizados neste trabalho são representados pelas letras: A, B, C e D.


## 1.2. Pré-requisitos

Para a execução do sistema piloto é necessário ter o software Python instalado. O arquivo de instalação pode ser obtido através do endereço: https://www.python.org/downloads/. É importante também adicionar o Python à configuração de PATH do sistema operacional. No Windows essa configuração pode ser realizada automaticamente selecionando a opção  “add Python to PATH” no início da instalação do Python.

Para a execução também é necessário a instalação de alguns módulos utilizados no código. Para facilitar essa instalação foi criado o arquivo “requerimentos.txt” que automatiza as instalações individuais. Para executar esse arquivo é necessário abrir o prompt de comando e digitar:
pip install -r requirements.txt


## 1.3. Execução

Após a instalação do Python e dos pacotes necessários o sistema piloto pode ser executado pelo prompt de comando. Na execução deve ser passado como parâmetro o índice da sentença no arquivo sentenças.txt. O exemplo abaixo apresenta a execução do sistema utilizando a sentença de índice 0 (zero).

_python CreateAnimation.py -sentenca 0_

O sistema irá gerar o arquivo da animação facial para ser executado pelo avatar. O nome do arquivo inicia com os caracteres EF seguido do índice da sentença processada e possui a extensão npy (matriz NumPy). Os arquivos das animações são salvos, por padrão, no diretório “dados\animacoesProntas\” localizado na raiz do sistema.

Relatório e gráfico da execução
Durante a execução do programa é exibido um relatório textual com informações sobre a execução do sistema e ao final um gráfico com o deslocamento do eixo X de um marcador da sobrancelha ao longo dos quadros de animação. Tanto o marcador quanto o eixo podem ser alterados na Seção denominada “Representação gráfica” no código. O trecho de código abaixo indica que será exibido o eixo X do marcador de índice 10.

_axis2Print = [True, False, False]_

_marker2Print = 10_

O marcador a ser exibido pode ser escolhido através da alteração da variável “marker2Print” com um valor entre 0 e 38. É possível também escolher o(s) eixo(s) a ser(em) exibido(s) através da alteração dos valores da lista “axis2Print”. Essa lista contém 3 valores boleanos indicando a execução dos eixos x, y e z respectivamente. O valor True indica o eixo que deve ser exibido e o valor False o eixo que não deve ser exibido.


# 2. Execução da animação facial pelo avatar

No texto abaixo serão apresentados os procedimentos para a execução, pelo avatar sinalizante, das animações faciais produzidas pelo sistema piloto. As animações faciais acompanham as animações corporais já inseridas no avatar sinalizante. Dessa forma, são disponibilizados arquivos criados no software Blender, do avatar já com as animações corporais para a execução dos procedimentos aqui apresentados. 

## 2.1. Pré-requisitos
Para a execução das animações é necessário ter instalado o software Blender que pode ser obtido pelo endereço: https://www.blender.org/. 
Os experimentos aqui apresentados foram realizados na versão do Blender 2.93.4.


## 2.2. Execução

Os arquivos de animação do Blender, estão salvos de forma compactada (no formato rar) no repositório do gitHub e devem ser descompactados no diretório rais do sistema piloto. Após descompactado, ao abrir o arquivo do avatar com a animação corporal no Blender é exibido, na aba _Scripting_, o avatar no painel à esquerda e o script responsável pela incorporação da animação facial no painel à direita. Abaixo do painel do avatar se encontra o painel de linha de tempo, que permite a execução da animação.

No script, a variável _sentence_ indica o nome do arquivo (sem sua extensão) que contém os dados da animação facial, criada pelo sistema piloto, a ser incorporada ao avatar. Na variável _dispPath_ é armazenado o caminho do arquivo de animação. Essa variável deve ser alterada de acordo com o local em que foi salvo o arquivo.

A execução do script é realizada através do atalho _Alt+P_ ou por um clique no botão marcado _run script_ na parte superior do painel de script. Após a execução é possível verificar as animações arrastando o cursor na barra do painel da linha de tempo ou clicando no botão de _play Animation_. 


# -*- coding: utf-8 -*-
"""
Sistema piloto de criação de animação facial.

Autor: Ackley Dias Will
"""

import numpy as np
import matplotlib.pyplot as plt
import pathlib
import os
import argparse


def hermiteCurve(P1,P2,TT,tg1,tg2):
    """
    Calcula e retorna a curva paramétrica cúbica de Hermite dadas as informações iniciais.
    
    Parâmetros:
        P1: Primeiro ponto da curva
        P2: Último ponto da curva
        TT: Comprimento da curva (quantidade de quadros)
        tg1: Tagente do primeiro ponto da curva
        tg2: Tangente do último ponto da curva
    
    Retorno:
        previous: Sinal posterior ao passado por parâmetro
    """
    VTT = np.array([TT,TT,TT])
    hermitMat = np.array([[2,-2,1,1],[-3,3,-2,-1],[0,0,1,0],[1,0,0,0]])   
    controlPoints = [P1,P2,VTT*(tg1),VTT*(tg2)]
    m = []
    TT += 1
    for i in range(1,TT):
        t = float(i)/TT
        vt = np.array(np.transpose([t**3,t**2,t,1]))
        m.append(vt.dot(hermitMat.dot(controlPoints)))
    return m


def sortFEList(expres): 
    """
    Coloca a lista com os dados das Expressões Faciais em ordem. Da Última para a primeira.
    
    Parâmetro:
        expres: Lista das expressões faciais - original
        
    Retorno:
        anim: Lista de expressões faciais - ordenada
    """
    newExpres = np.zeros_like(expres)
    used=[]
    for i in range(len(expres)):
        maior= 0
        for ef in expres:
            if ef[2]>maior and ef[2] not in used:
                maior=ef[2]
                newExpres[i] = ef
        used.append(maior) 
    return newExpres              


def makeAnimation(signFrames, expres):
    """
    Cria a animação final incluindo as expressões faciais e suas transições.
    
    Parâmetros:
        signFrames: Dados de entrada formatados 
        expres: Expressões faciais selecionadas
        
    Retorno:
        anim: Animação facial final
    """
    length = signFrames[-1][1] + signFrames[-1][2] # tamanho total da animação corporal
    markers = len(expres[0][0][0]) # Quantidade de marcadores
    anim = np.zeros(([length+200,markers,3]))
    expres = sortFEList(expres) 
    contEF = 0
    P2 = []
    T2n = []
    cont=-1
    for ef in expres:
        cont+=1
        framesT1, framesT2 = ef[3][0], ef[3][1]
        firstFrame = 0 # Primeiro quadro do sinal (primeiro da transicao inicial)
        trans1 = createTransition(ef[0],markers,framesT1,firstFrame,P2,T2n)  
        firstFrame = -1 # Último quadro do sinal (primeiro da transicao Final)
        trans2 = createTransition(ef[0],markers,framesT2,firstFrame,P2,T2n)   
        P2 = ef[0][0]
        T2n = ef[0][1]
        signal = list(trans1[:].copy()) + list(ef[0].copy()) + list(trans2.copy())
        if (anim[ef[2]+len(signal)-len(trans1)][0][0] == 0): # Transição 2 irá para 0 caso seu comprimento não toque outro sinal
            trans2 = createTransition(ef[0],markers,framesT2,firstFrame,[],[]) 
            signal = list(trans1.copy()) + list(ef[0].copy()) + list(trans2.copy())
        contEF+=1
        anim[ef[2]-len(trans1):ef[2]+len(signal)-len(trans1)] = signal
        anim[ef[2]-len(trans1):ef[2]+len(signal)-len(trans1)] = signal
    return anim


def createTransition(ef,markers,framesTrans,firstFrame,P2n,T2n):
    """
    Cria a animação da transição a direita e a esquerda dos sinais utilizando a função da curva de Hermite.
    
    Parâmetros:
        ef: Animação da expressão facial
        markers: Número total de marcadores
        framesTrans: Comprimento da transição a ser criada
        firstFrame: Indicação se a transição a ser criada é a esquerda (-1) ou a direita (0) da animação
        P2n: Posições dos marcadores no primeiro quadro da animação anterior
        T2n: Posições dos marcadores no segundo quadro da animação anterior
        
    Retorno:
        trans: animação da transição criada
    """
    marker = []
    for m in range(markers):# para cada marcador 
        if (firstFrame==0): # Transição à ESQUERDA do sinal (firstFrame == 0)
            P1 = [0.0,0.0,0.0] 
            T1 = [0.0, 0.0, 0.0]
            P2 = ef[0][m] 
            T2 = ef[1][m]-ef[0][m]
        else: # Transição à DIREITA do sinal (firstFrame == -1)
            P1 = ef[-1][m] 
            T1 = ef[-1][m]-ef[-2][m]
            P2 = [0.0,0.0,0.0]
            T2 = [0.0,0.0,0.0]
            if len(P2n) > 0: # a partir da primeira EF da sequencia
                P2 = P2n[m]
                T2 = T2n[m]-P2n[m]
        t1 = hermiteCurve(P1,P2,framesTrans,T1,T2)
        marker.append(t1)
    trans = np.zeros(([framesTrans,markers,3]))
    for f in range(framesTrans):
        for m in range(markers):
            trans[f][m] = marker[m][f]
    return trans


def readSentenceTimes(path):
    """
    Lê os dados de entrada a partir do arquivo indicado por path.
    
    Parâmetros:
        path: caminho do arquivo com os dados de entrada
        
    Retorno:
        sentenceTimes: Sentenças e instantes de início dos sinais e transições
    """
    sentenceTimes = []
    file = open(path,'r')   
    cont=0
    for line in file:
        if cont>1:
            cont=0
        if cont == 0:
            line = line[:-1]
            sentence = line.split(' ')
        elif cont == 1:
            timeStrs = line.split(',')
            timeStarts = []
            times = []
            for i in range(len(timeStrs)):
                timeStarts.append(int(timeStrs[i][1:]))
                if i==0:
                    times.append(int(timeStrs[i][1:]))
                elif i<len(timeStrs)-1:
                    times.append(int(timeStrs[i+1][1:]) - int(timeStrs[i][1:]))
            sentenceTimes.append([sentence,timeStarts,times])
        cont+=1             
    file.close()
    return sentenceTimes


def getTimeAndDurationOfAnExpression(sentenceIndex, sentences):
    """
    Calcula os dados de cada sinal da animação [posição, duração, duração da transição a esquerda e a direita].
    
    Parâmetros:
        sentenceIndex: Indice da animação no arquivo de sentenças (dados de entrada)
        sentences: Caminho do arquivo de senteças e anotações de tempos
        
    Retorno:
        singInfo: Dados de entrada formatados 
    """
    data = readSentenceTimes(sentences)
    sentence = data[sentenceIndex][0]
    singInfo=[]
    for i in range(len(sentence)):
        sign = sentence[i].upper()
        if sign=='?':
            pos = len(data[sentenceIndex][0])-1
        else:
            pos = data[sentenceIndex][0].index(sign)
        dur = data[sentenceIndex][2][pos*2+1]
        start = data[sentenceIndex][1][pos*2+1]
        durT1 = start - data[sentenceIndex][1][pos*2]
        durT2 = data[sentenceIndex][1][pos*2+3]-data[sentenceIndex][1][pos*2+2]
        singInfo.append([sign,start,dur,durT1,durT2])
    return singInfo
    
    
def getSignalsWFE(rules, signFrames):
    """
    Verifica os dados dos sinais que possuem expressões faciais.
    
    Parâmetros:
        rules: Caminho do arquivo com as regras (banco de regras)
        signFrames: Dados de entrada formatados 
        
    Retorno:
        singInfo: Sinais que possuem expressões faciais, seus tipos e comprimento das animações
    """
    interr = False
    if signFrames[-1][0][-1] == '?': # Sentença interrogativa
        interr = True
        signFrames[-1][0] = signFrames[-1][0][:-1]
    foundSings = []
    toRemove = []
    EFFile = open(rules,'r')
    EFSigns = []
    for line in EFFile:
        line = line[:-1].split(" ")
        if line[0]=='*?' or line[0][-1]=='*':
            ruleYesNo = line[1]
        for s in range(len(signFrames)): # Verifica se o sinal no arquivo de exp faciais está na sentença
            signs = signFrames[s]
            if line[0][-1] == '?' and interr:
                sign = line[0][:-1]
                if sign in signs:
                    foundSings.append(sign)
                    EFSigns.append([sign,line[1],signs[1],signs[2],signs[3],signs[4]]) 
                    # Caso exista uma regra que inclua sinais anteriores e esses sinais tenham expressões 
                    # faciais próprias, essas expressões são marcadas para remoção
                    if len(line[1]) > 2:
                        # print('\nComposta')
                        # print(line[1])
                        for j in range(s-1,s-1-int(line[1][3]),-1): 
                            # print(signFrames[j])
                            toRemove.append(signFrames[j][0])
            elif line[0] in signs and line[0] not in foundSings:
                foundSings.append(line[0])
                EFSigns.append([line[0],line[1],signs[1],signs[2],signs[3],signs[4]])
                # Caso exista uma regra que inclua sinais anteriores e esses sinais tenham expressões 
                # faciais próprias, essas expressões são marcadas para remoção
                if len(line[1]) > 2:
                    # print('\nComposta')
                    # print(line[1])
                    for j in range(s-1,s-1-int(line[1][3]),-1): 
                        print(signFrames[j])
                        toRemove.append(signFrames[j][0])     
    if interr and signFrames[-1][0] not in foundSings:
        EFSigns.append([signFrames[-1][0],ruleYesNo,signFrames[-1][1],signFrames[-1][2],signFrames[-1][3],signFrames[-1][4]]) 
    EFFile.close()
    EFList =[]
    # print(EFSigns)
    # print(toRemove)
    for i in range(len(EFSigns)): # Remove as exp faciais marcadas (já existentes por uma regra aplicada a um sinal diferente)
        if EFSigns[i][0] not in toRemove:
            EFList.append(EFSigns[i])
    return EFList
  

def previousSign(sign):
    """
    Retorna o nome do sinal anterior ao passado como parâmetro.
    
    Parâmetros: 
        sign: Sinal posterior ao que se deseja buscar
    
    Retorno:
        previous: Sinal posterior ao passado por parâmetro
    """
    previous = 'None'
    for s in range(len(signFrames)):
        if signFrames[s][0]==sign:
            previous = signFrames[s-1][0]
    return previous
          

def selectAnimations(signalsWithFacialExpressions,expressions,signFrames):
    """
    Seleciona os trechos das expressões faciais que farão parte da animação final.
    
    Parâmetros:
        signalsWithFacialExpressions: Dados dos sinais que contém expressões faciais
        expressions: Caminho do repositório das expressões faciais (trechos de animações)
        signFrames:  Dados de entrada formatados 
        
    Retorno:
        animations: Animações selecionadas com os dados de posição e comprimento das transiçÕes à esquerda e à direita
    """
    folders = pathlib.Path(expressions)
    animations = []
    for j in range(len(signalsWithFacialExpressions)):
        for s in range(len(signFrames)):
            if signalsWithFacialExpressions[j][0] == signFrames[s][0]:
                EFidx = s-len(signFrames)+1
        lastEfNum = -1 # controle da posição de aplicação da exp facial
        for i in range(0,len(signalsWithFacialExpressions[j][1]),2): # Busca cada expressão facial na regra. Exemplo B1A1 busca as expressões B e A
            EFID = signalsWithFacialExpressions[j][1][i]
            if i==0:
                print("Sinal: "+ signalsWithFacialExpressions[j][0])
            else:
                print("Sinal: "+ previousSign(signalsWithFacialExpressions[j][0]) + " (da regra aplicada ao sinal",signalsWithFacialExpressions[j][0]+")" )
            print('\nExpressão facial do tipo '+EFID)
            numSigns = int(signalsWithFacialExpressions[j][1][i+1])
            EFidx += lastEfNum
            posEF = signFrames[EFidx][1]
            lenEF = signFrames[EFidx][2]
            for c in range(1,numSigns):
                lenEF += signFrames[EFidx+c][2]
            lenTrans1 = signFrames[EFidx][3]
            lenTrans2 = signFrames[EFidx][4]
            print('\nTransição inicial: '+ str(lenTrans1))
            print('Transição final: ' + str(lenTrans2) + '\n')
            files = folders.glob(EFID+'*')
            diff = signFrames[-1][1] + signFrames[-1][2] # Tamanho total da animação corporal   
            first = True
            print('Animações (Expressões faciais) no repositório: ')
            cont=1
            choosedFile = 'None!'
            choosedAnim = 'None!'
            for f in files:
                if first:
                    choosedAnim = np.load(f)
                    first = False
                anim = np.load(f)
                lenExp = len(anim) # Comprimento da animação da exp Facial do arquivo buscado
                diffTemp = np.abs(lenExp-lenEF)
                print("    "+str(f)[-6:-4] +" - Duração: " + str(lenExp) + " - Diferença: " + str(diffTemp))
                cont+=1
                if (diffTemp<diff):
                    diff=diffTemp
                    choosedAnim = anim.copy()
                    choosedFile = f
            print('\nAnimação escolhida: ' + str(choosedFile)[-6:])
            anim = adjustAnimation(choosedAnim, lenEF)
            animations.append([anim,lenEF,posEF,[lenTrans1,lenTrans2]])
    return animations
            

def adjustAnimation(anim, lenEF):
    """
    Ajusta o comprimento dos trechos de animações para se adequarem ao comprimento dos sinais.
    
    Parâmetros:
        anim: Animação escolhida no banco de expressões faciais
        lenEF: comprimento que a animação deverá se ajustar
        
    Retornos:
        anim: Trecho da animação original (caso não precise de ajustes)
        newAnim: Trecho da animação com o comprimento ajustado
    """
    diff = len(anim) - lenEF
    print('\nDuração esperada: %s  -  Duração da animação escolhida: %s'%(lenEF, len(anim)))
    if diff<0: 
        diff = np.abs(diff)
        print('\n-------------------------------')
        print("Aplicação de aumento da duração")
        print("  Tamanho Original: "+str(len(anim)))
        newAnim = []
        insert = int(len(anim)/np.abs(diff))
        cont=0
        j=0
        for i in range(lenEF):
            if cont==insert-1:
                cont=-1
                newAnim.append(anim[j])
            else:
                newAnim.append(anim[j])
                j+=1
            cont+=1           
        print('  Duração da animação ajustada: ' + str(len(newAnim)))
        print('-------------------------------\n')
        return newAnim
    elif diff>0:
        print('\n-------------------------------')
        print("Aplicação de redução da duração")
        print("  Tamanho Original: "+str(len(anim)))
        newAnim = []
        stepOriginal = int(len(anim)/diff)
        step = stepOriginal
        rest = (len(anim)/diff)- int(len(anim)/diff)
        somaRest = 0
        for i in range(len(anim)):
            if len(newAnim)>=lenEF:
                break
            if i%step!=0:
                newAnim.append(anim[i])
                somaRest += rest
                step = stepOriginal
            if(somaRest>=1):
                somaRest = somaRest-1
                step+=1
        rest = lenEF-len(newAnim)
        for i in range(rest):
            newAnim.append(anim[-1])
       
        print('  Duração da animação ajustada: ' + str(len(newAnim)))
        print('-------------------------------\n')
        return newAnim
    else:
        return anim
    
    
def plotSignal(signal, marker,axis2Print,step=2,capV='Deslocamento',capH='Número de quadros',title='Deslocamento ao longo dos quadros'):
    """
    Apresenta o gráfico de deslocamento, ao longo dos quadros de animação, de um determinado sinal e sinal.
    
    Parâmetros:
        signal: Animação
        marker: Marcador escolhido
        axis2Print: Eixo escolhido
        step: Intervalo no eixo de quadros
        capV: legenda do eixo vertical
        capH: Legenda do eixo horizontal
    """
    x,y,z = [],[],[]
    
    for a in signal:
        x.append(a[marker][0])   
        y.append(a[marker][1])
        z.append(a[marker][2])
    # plt.figure(figsize=(25,8)) 
    plt.figure(figsize=(12,8)) 
    # plt.figure(figsize=(6,4)) 
    # plt.figure(figsize=(16.8,11.2)) 
    plt.xlabel(capH) 
    plt.ylabel(capV)
    
    dim=np.arange(0,len(signal),step)
    plt.xticks(dim)
    plt.grid()
    if axis2Print[0]:    
        plt.title(title)
        plt.ylabel(capV + ' no eixo X')
        plt.plot(x)
        plt.show()
    if axis2Print[1]:
        plt.title(title)
        plt.ylabel(capV + ' no eixo Z')
        plt.plot(y)
        plt.show()
    if axis2Print[2]:
        plt.title(title)
        plt.ylabel(capV + ' no eixo Y')
        plt.plot(z)
        plt.show()
    plt.close()
    
    
###################  Parâmetros iniciais  #####################################################################################################################

path =        os.getcwd() + '/dados/'    # Caminho do diretório raiz dos dados
sentences =   path + 'dadosEntrada/sentencas.txt'                       # Sentenças e anotações dos tempos (dados de entrada)
rules =       path + 'bancoRegras/regras.txt'                           # Banco de regras
expressions = path + 'repositorioExpressoes/'                           # Repositório de expressões faciais


# índice da sentença obtido por parâmetro na execução.
# Exemplo de execução para a sentença 0: 
#    python CreateAnimation.py -sentenca 0
parser = argparse.ArgumentParser(description='Teste arg')
parser.add_argument('-sentenca', "-i",required=True, help= "Índice da sentença no arquivo sentencas.txt")
sentenceIndex = int(parser.parse_args().sentenca)                       # Índice da sentença no arquivo de sentenças


###################   Execução   ##############################################################################################################################

signFrames = getTimeAndDurationOfAnExpression(sentenceIndex, sentences)
print('\nDados de entrada formatados:')
print(signFrames)
signalsWithFacialExpressions = getSignalsWFE(rules, signFrames) 
print('\nSinais com expressões faciais:')
print(signalsWithFacialExpressions)
FEAnimations = selectAnimations(signalsWithFacialExpressions,expressions,signFrames) 
anim = makeAnimation(signFrames, FEAnimations) 


################### Representação gráfica  ####################################################################################################################

fLabels = open(expressions + 'labels.lbl','r')
labels = (str(fLabels.readlines()[0])).split(",")
fLabels.close()
animRange = [0,-1] # padrão [0,-1]

axis2Print = [True, False, False] # Quais eixos devem ser mostrados [ X, Y, Z]
marker2Print = 10
plotSignal(anim[animRange[0]:animRange[1]],marker2Print,axis2Print,step=50, title ='Marcador: %s (%d)'%(labels[marker2Print],marker2Print))


###################  Gravação da animação   ###################################################################################################################

# np.save(path+'animacoesProntas/EF'+str(sentenceIndex),anim)
# print('\nArquivo de animação salvo com sucesso!')
# print('   Caminho do arquivo:',path+'animacoesProntas/')
# print('   Nome do arquivo: EF'+str(sentenceIndex) +'.npy')

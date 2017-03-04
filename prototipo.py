"""
Prototipo do VisualiZe
"""

# Importando bibliotecas necessarias
import os
import nibabel as nib
from matplotlib import pyplot as plt
import pickle
from matplotlib.widgets import Button


# Definindo diretorio com os exames a serem analisados
data_dir = os.path.expanduser('~') + '/' + 'Downloads' + '/'

# Diretorio para guardar a estrutura com os dados de classificacao
out_dir = os.path.expanduser('~') + '/' + 'Downloads' + '/'

# Listando sujeitos a serem analisados
subjects = ['SCHB009']

# Criando variavel para loop while
#direc = 0
#sl = 0

####Classe botoes
class Index(object):

    def bom(self, event):
        print 'Imagem boa.'
        dados.append(1)
        sl = sl + 1
        raise Clique

    def ruim(self, event):
        print 'Imagem ruim.'
        dados.append(2)
        sl = sl + 1
        raise Clique

    def voltar(self, event):
        print 'Retornando a imagem anterior'
        sl = sl - 1
        del dados[-1]
        raise Clique
#####

# Excecao para ver clique do mouse
class Clique(Exception):
    pass


# Iniciando laco para repetir processamento para cada sujeito
for subj in subjects:

    # Criando lista para guardar dados do sujeito
    dados = []

    # Definindo caminho para a imagem do sujeito
    img_file = data_dir + subj + '/' + subj + '.nii.gz'
    # Carregando a imagem no ambiente Python
    img = nib.load(img_file)
    # Carregando os dados da imagem
    img_data = img.get_data()
    # Extraindo informacoes das dimensoes da imagem
    sizeX, sizeY, numSlices, numDir = img_data.shape

    # Criando variavel para loop while
    direc = 0
    sl = 0

    # Criando objeto para rotinas de botao
    callback = Index()

    # Definindo caminho para a fft da imagem do sujeito
    fft_file = data_dir + subj + '/' + 'fft' + '.nii.gz'
    # Carregando a imagem no ambiente Python
    fft = nib.load(fft_file)
    # Carregando os dados da imagem
    fft_data = fft.get_data()

    # Inicializa-se a janela antes do loop para nao precisar recarregar todo o plot a cada iteracao
    fig = plt.figure()

    # Iniciando laco para repetir processamento para cada direcao
    while (direc < numDir):
        # Trabalhando slice a slice na direcao
        while (sl < numSlices):
            # Separando slice de interesse do volume
            slice = img_data[:,:,sl,direc]
            # Normalizando intensidades do slice para soma ser 1000000
            slice = slice / (slice.sum()/1000000)
            # Separando a fft do slice
            slice_fft = fft_data[:,:,sl,0,direc]
            # Colocando as frequencias mais baixas no centro
            # slice_fft = fftpack.fftshift(slice_fft)
            # Mostrando uma figura com as imagens de interesse
            fig.clear()
            fig.suptitle('Sujeito %s Direcao %d Slice %d' % (subj, direc, sl), fontsize=16)
            ax1 = fig.add_subplot(121)
            ax1.imshow(slice,cmap='gray')
            ax1.set_title('Espaco')
            ax1.axes.xaxis.set_visible(False)
            ax1.axes.yaxis.set_visible(False)

            ax2 = fig.add_subplot(122)
            ax2.imshow(slice_fft,cmap='gray')
            ax2.set_title('Frequencia')
            ax2.axes.xaxis.set_visible(False)
            ax2.axes.yaxis.set_visible(False)


            bom = plt.axes([0.5, 0.05, 0.1, 0.075])
            ruim = plt.axes([0.61, 0.05, 0.1, 0.075])
            voltar = plt.axes([0.81, 0.05, 0.1, 0.075])

            botao_bom = Button(bom, 'Bom')
            botao_bom.on_clicked(callback.bom)

            botao_ruim = Button(ruim, 'Ruim')
            botao_ruim.on_clicked(callback.ruim)

            botao_voltar = Button(voltar, 'Voltar')
            botao_voltar.on_clicked(callback.voltar)

            #Isso libera o terminal para os comandos
            plt.show(block=False)
            #Isto redesenha a figura a cada iteracao
            fig.canvas.draw()
            try:
                string = raw_input("[1] Boa/[2] Ruim ou [3] para retornar: ")
                if (int(string) == 1):
                    print 'Imagem boa.'
                    dados.append(1)
                    sl = sl + 1
                elif (int(string) == 2):
                    print 'Imagem ruim.'
                    dados.append(2)
                    sl = sl + 1
                elif (int(string) == 3):
                    print 'Retornando a imagem anterior'
                    sl = sl - 1
                    del dados[-1]
                else:
                    print 'Digite um comando valido.'
            except(ValueError):
                pass
            except(Clique):
                continue
    # Fechando janela com as figuras
    plt.close(fig)
# Salvando os dados em arquivo pickle
pickle.dump(dados,open(out_dir + "dados_%s.p" % subj,"wb"))

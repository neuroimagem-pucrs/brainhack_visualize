"""
Prototipo do VisualiZe
"""

# Importando bibliotecas necessarias
import os
import nibabel as nib
from matplotlib import pyplot as plt # para teste
import pickle # para teste
from Tkinter import *

#### botoes ####
# class Application(Frame):
#     def say_hi(self):
#         print "hi there, everyone!"
#
#     def createWidgets(self):
#         self.QUIT = Button(self)
#         self.QUIT["text"] = "QUIT"
#         self.QUIT["fg"]   = "red"
#         self.QUIT["command"] =  self.quit
#
#         self.QUIT.pack({"side": "left"})
#
#         self.hi_there = Button(self)
#         self.hi_there["text"] = "Hello",
#         self.hi_there["command"] = self.say_hi
#
#         self.hi_there.pack({"side": "left"})
#
#     def __init__(self, master=None):
#         Frame.__init__(self, master)
#         self.pack()
#         self.createWidgets()
#
# root = Tk()
# app = Application(master=root)
# app.mainloop()
# root.destroy()

################
#from matplotlib.backends.backend_pdf import PdfPages # para teste

# Definindo diretorio com os exames a serem analisados
data_dir = os.path.expanduser('~') + '/' + 'Downloads' + '/'

# Diretorio para guardar a estrutura com os dados de classificacao
out_dir = os.path.expanduser('~') + '/' + 'Downloads' + '/' +

# Listando sujeitos a serem analisados
subjects = ['SCHB009']

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
    sl = 0

    # Definindo caminho para a fft da imagem do sujeito
    fft_file = data_dir + subj + '/' + subj + '.nii.gz'
    # Carregando a imagem no ambiente Python
    fft = nib.load(fft_file)
    # Carregando os dados da imagem
    fft_data = fft.get_data()

    # Criando arrays para as coordenadas da imagem em 1D
    x = []
    y = []
    """
    for i in xrange(sizeX):
        for j in xrange(sizeY):
            x = np.append(x,i)
            y = np.append(y,j)
    xy = np.array([x,y])
    """

    # Inicializa-se a janela antes do loop para nao precisar recarregar todo o plot a cada iteracao
    fig = plt.figure()

    # Iniciando laco para repetir processamento para cada direcao
    for direc in [1]:#xrange(numDir):       #range(numDir)
        # Trabalhando slice a slice na direcao
        #for sl in xrange(20,30): #xrange(numSlices):
        while (sl < numSlices):
            # Separando slice de interesse do volume
            slice = img_data[:,:,sl,direc]
            # Normalizando intensidades do slice para soma ser 1000000
            slice = slice / (slice.sum()/1000000)
            # Separando a fft do slice
            slice_fft = fft_data[:,:,sl,direc]
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

            #Isso libera o terminal para os comandos
            plt.show(block=False)
            #Isto redesenha a figura a cada iteracao
            fig.canvas.draw()

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

    plt.close(fig)

pickle.dump(dados,open(out_dir + "dados_%s.p" % subj,"wb"))

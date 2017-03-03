"""
Prototipo do VisualiZe
"""

# Importando bibliotecas necessarias
import os
import nibabel as nib
from matplotlib import pyplot as plt # para teste
import pickle # para teste
#from matplotlib.backends.backend_pdf import PdfPages # para teste

# Definindo diretorio com os exames a serem analisados
data_dir = os.path.expanduser('~') + '/' + 'TCC' + '/' + 'Teste1' + '/'

# Diretorio para guardar a estrutura com os dados de classificacao
out_dir = os.path.expanduser('~') + '/' + 'TCC' + '/' + 'Teste1' + '/' + 'dados_classificados' + '/'

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

    # Definindo caminho para a fft da imagem do sujeito
    fft_file = data_dir + subj + '/' + 'fft' + '.nii.gz'
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

    # Iniciando laco para repetir processamento para cada direcao
    for direc in xrange(numDir):       #range(numDir)
        # Trabalhando slice a slice na direcao
        for sl in xrange(numSlices):     #range(numSlices)
            # Separando slice de interesse do volume
            slice = img_data[:,:,sl,direc]
            # Normalizando intensidades do slice para soma ser 1000000
            slice = slice / (slice.sum()/1000000)
            # Separando a fft do slice
            slice_fft = fft_data[:,:,sl,0,direc]
            # Colocando as frequencias mais baixas no centro
  #          slice_fft = fftpack.fftshift(slice_fft)

                # Mostrando uma figura com as imagens de interesse
            plt.clf()
            fig = plt.figure()
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

            plt.show()
# Aqui deve vir o comando para esperar a tecla ser pressionada                #dados.append(dados_temp)

            plt.close(fig)

    pickle.dump(dados,open(out_dir + "dados_%s.p" % subj,"wb"))

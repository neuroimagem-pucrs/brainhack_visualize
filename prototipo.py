"""
Protótipo do Visualizé
"""

# Importando bibliotecas necessarias
import os
import nibabel as nib
#from matplotlib import pyplot as plt # para teste
import pickle # para teste
#from matplotlib.backends.backend_pdf import PdfPages # para teste

# Definindo diretorio com os exames a serem analisados
data_dir = os.path.expanduser('~') + '/' + 'Dropbox' + '/' + 'UFRGS' + '/' + 'TCC' + '/' + 'Teste1' + '/'

out_dir = os.path.expanduser('~') + '/' + 'Dropbox' + '/' + 'UFRGS' + '/' + 'TCC' + '/' + 'results' + '/'

# Listando sujeitos a serem analisados
subjects = ['SCHB038']

# Iniciando laco para repetir processamento para cada sujeito
for subj in subjects:

    # Criando lista para guardar dados do sujeito
    dados = []

    # Criando pdf com figuras
#    pp = PdfPages('figuras_%s.pdf' % subj)

    # Definindo caminho para a imagem do sujeito
    img_file = data_dir + subj + '/' + subj + '.nii.gz'
    # Carregando a imagem no ambiente Python
    img = nib.load(img_file)
    # Carregando os dados da imagem
    img_data = img.get_data()
    # Extraindo informacoes das dimensoes da imagem
    sizeX, sizeY, numSlices, numDir = img_data.shape

    # Criando arrays para as coordenadas da imagem em 1D
    x = []
    y = []
    for i in xrange(sizeX):
        for j in xrange(sizeY):
            x = np.append(x,i)
            y = np.append(y,j)
    xy = np.array([x,y])

    # Iniciando laco para repetir processamento para cada direcao
    for direc in xrange(numDir):       #range(numDir)
        # Trabalhando slice a slice na direcao
        for sl in xrange(numSlices):     #range(numSlices)
            # Iniciando o timer para o slice
#            start_slice = time.time()
            # Separando slice de interesse do volume
            slice = img_data[:,:,sl,direc]
            # Normalizando intensidades do slice para soma ser 10000000
            # slice = slice / (slice.sum()/10000000)
            # Fazendo a fft do slice
            slice_fft = fftpack.fft2(slice)
            # Colocando as frequencias mais baixas no centro
            slice_fft = fftpack.fftshift(slice_fft)
            # Calculando o espectro de potencia
            ps = np.abs(slice_fft)**2
            # Normalizando o espectro para 100
            ps = ps / (ps.sum()/100)
            # Analisando o perfil radial do espectro
#            rp = radialProfile.azimuthalAverage(ps)

            # Transformando espectro em sequencia de pontos
            ps_1D = np.ravel(ps)

            # Definindo uma estimativa inicial para o ajuste
            # Parametros [amp,x0,y0,a,b,c]
            guess = [1,128,128,1,1,1]

            try:
                fit_params, uncert_cov = opt.curve_fit(gauss2d,xy,ps_1D,p0=guess)

                # Calculando a gaussiana dada pelo ajuste
                ps_fit = gauss2d(xy,*fit_params)
                # Calculando o RMS do residuo do ajuste
                resid = np.sqrt(np.mean((ps_1D - ps_fit)**2))


                # Salvando os dados do ajuste
                dados_temp = [subj,direc,sl,fit_params,uncert_cov,resid]
                dados.append(dados_temp)

                """
                # Mostrando uma figura com as imagens de interesse
                plt.clf()
                fig = plt.figure()
                fig.suptitle('Sujeito %s Direcao %d Slice %d' % (subj, direc, sl), fontsize=16)
                ax1 = fig.add_subplot(131)
                ax1.imshow(slice,cmap='gray')
                ax1.set_title('%f - %f'% (fit_params[0],fit_params[4]))
                ax1.axes.xaxis.set_visible(False)
                ax1.axes.yaxis.set_visible(False)
                ax2 = fig.add_subplot(132)
                ax2.imshow(np.log10(ps))#,cmap='gray')
                ax2.set_title('%f - %f'% (fit_params[3],fit_params[5]))
                ax2.axes.xaxis.set_visible(False)
                ax2.axes.yaxis.set_visible(False)
                ax3 = fig.add_subplot(133)
                ax3.semilogy(rp)
                ax3.set_title('Perfil Radial')
                ax3.set_xlabel('Frequencia Espacial')
                ax3.set_ylabel('Magnitude')
                #plt.show()
                pp.savefig()
                plt.close(fig)
                """

            except RuntimeError:
                erros.append([subj,direc,sl])
                print('Parametros otimos nao encontrados!!')
                print('Seguindo adiante!')
                # Salvando os dados do ajuste
                dados_temp = [subj,direc,sl,'erro','erro','erro']
                dados.append(dados_temp)

                """
                # Mostrando uma figura com as imagens de interesse
                plt.clf()
                fig = plt.figure()
                fig.suptitle('Sujeito %s Direcao %d Slice %d' % (subj, direc, sl), fontsize=16)
                ax1 = fig.add_subplot(131)
                ax1.imshow(slice,cmap='gray')
                ax1.set_title('erro')
                ax1.axes.xaxis.set_visible(False)
                ax1.axes.yaxis.set_visible(False)
                ax2 = fig.add_subplot(132)
                ax2.imshow(np.log10(ps))#,cmap='gray')
                ax2.set_title('erro')
                ax2.axes.xaxis.set_visible(False)
                ax2.axes.yaxis.set_visible(False)
                ax3 = fig.add_subplot(133)
                ax3.semilogy(rp)
                ax3.set_title('Perfil Radial')
                ax3.set_xlabel('Frequencia Espacial')
                ax3.set_ylabel('Magnitude')
                #plt.show()
                pp.savefig()
                plt.close(fig)
                """

    pickle.dump(dados,open(out_dir + "dados_%s.p" % subj,"wb"))
#    pp.close()

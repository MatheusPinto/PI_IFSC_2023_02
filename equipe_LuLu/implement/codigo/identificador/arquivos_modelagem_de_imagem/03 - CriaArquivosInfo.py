import os

def CriarInfo_pos_e_neg():
    """Cria um arquivo info para imagens positivas e negativas.

    * Para o arquivo positivo determina arquivo Info.dat (Informação positiva da imagem)
    * Para o arquivo negativo determina arquivo bg.txt (Background/Fundo)
    """
    for file_type in ['negativo']:
        for img in os.listdir(file_type):
            if file_type == 'positivo':
                line = file_type+'/'+img+' 1 0 0 50 50\n'
                with open('info.dat', 'a') as f:
                    f.write(line)
                    # Caso imagem positiva, determina o local onde a mesma se encontra na imagem, e esta informação é salva no arquivo info.dat.
            elif file_type == 'negativo':
                line = file_type+'/'+img+'\n'
                with open('bg.txt', 'a') as f:
                    f.write(line)
                    # Caso imagem negativa, a informação é salva no arquivo bg.txt significando que a mesma é um fundo não desejado.
CriarInfo_pos_e_neg()
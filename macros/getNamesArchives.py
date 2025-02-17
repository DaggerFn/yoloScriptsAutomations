import os

def listar_arquivos(diretorio):
    try:
        # Obtém a lista de arquivos no diretório especificado
        arquivos = os.listdir(diretorio)
        
        # Filtra apenas arquivos (ignora diretórios)
        arquivos = [arquivo for arquivo in arquivos if os.path.isfile(os.path.join(diretorio, arquivo))]
        
        # Exibe os nomes dos arquivos
        print("Arquivos no diretório '{}':".format(diretorio))
        for arquivo in arquivos:
            print(arquivo)
        
    except Exception as e:
        print(f"Ocorreu um erro ao acessar o diretório: {e}")

# Especifique o diretório que você quer analisar
diretorio = r'C:\Users\gustavonc\Documents\GitHub\yolo-training-boxes\dataset'  # Substitua pelo caminho do seu diretório

listar_arquivos(diretorio)

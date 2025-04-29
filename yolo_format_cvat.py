#!/usr/bin/env python3
import os
import shutil

# Configurações definidas via variáveis:
INPUT_DIR = r"C:\Users\gustavonc\Downloads\AutoAnnotate\labels"       # Diretório onde estão as imagens e labels
OUTPUT_DIR = r"C:\Users\gustavonc\Downloads\AutoAnnotate\yolo_formater"          # Diretório onde será criada a estrutura de saída
SUBSET = "train"                          # Pode ser "train" ou "valid"
CLASSES = ["motor", "hand"]        # Lista de classes

def criar_estrutura_saida(output_dir, subset):
    """
    Cria a estrutura de pastas e arquivos de saída.
    """
    archive_dir = os.path.join(output_dir, "archive")
    os.makedirs(archive_dir, exist_ok=True)
    
    subset_folder = f"obj_{subset}_data"
    subset_dir = os.path.join(archive_dir, subset_folder)
    os.makedirs(subset_dir, exist_ok=True)
    
    backup_dir = os.path.join(archive_dir, "backup")
    os.makedirs(backup_dir, exist_ok=True)
    
    return archive_dir, subset_dir, backup_dir, subset_folder

def criar_train_valid_file(archive_dir, subset_folder, image_files, subset):
    """
    Cria o arquivo train.txt ou valid.txt com os caminhos das imagens.
    """
    txt_filename = f"{subset}.txt"
    txt_path = os.path.join(archive_dir, txt_filename)
    with open(txt_path, "w") as f:
        for image in image_files:
            f.write(f"{subset_folder}/{image}\n")
    return txt_filename

def criar_obj_data(archive_dir, num_classes, train_txt, backup_folder):
    """
    Cria o arquivo obj.data com as configurações.
    """
    data_path = os.path.join(archive_dir, "obj.data")
    with open(data_path, "w") as f:
        f.write(f"classes = {num_classes}\n")
        f.write("names = obj.names\n")
        f.write(f"train = {train_txt}\n")
        f.write(f"backup = {os.path.basename(backup_folder)}/\n")
    return data_path

def criar_obj_names(archive_dir, classes):
    """
    Cria o arquivo obj.names com os nomes das classes.
    """
    names_path = os.path.join(archive_dir, "obj.names")
    with open(names_path, "w") as f:
        for nome in classes:
            f.write(f"{nome.strip()}\n")
    return names_path

def processar_arquivos(input_dir, subset_dir):
    """
    Copia os arquivos de imagem e seus respectivos arquivos de label (se existirem) para a pasta de saída.
    Retorna a lista dos nomes dos arquivos de imagem copiados.
    """
    exts = (".jpg", ".jpeg", ".png", ".bmp")
    imagens_copiadas = []
    
    for arquivo in os.listdir(input_dir):
        if arquivo.lower().endswith(exts):
            caminho_imagem = os.path.join(input_dir, arquivo)
            destino_imagem = os.path.join(subset_dir, arquivo)
            shutil.copy2(caminho_imagem, destino_imagem)
            imagens_copiadas.append(arquivo)
            
            base, _ = os.path.splitext(arquivo)
            label_filename = base + ".txt"
            caminho_label = os.path.join(input_dir, label_filename)
            if os.path.exists(caminho_label):
                destino_label = os.path.join(subset_dir, label_filename)
                shutil.copy2(caminho_label, destino_label)
    
    return imagens_copiadas

def main():
    num_classes = len(CLASSES)
    
    archive_dir, subset_dir, backup_dir, subset_folder = criar_estrutura_saida(OUTPUT_DIR, SUBSET)
    
    imagens = processar_arquivos(INPUT_DIR, subset_dir)
    if not imagens:
        print("Nenhuma imagem encontrada no diretório de entrada.")
        return
    
    subset_txt = criar_train_valid_file(archive_dir, subset_folder, imagens, SUBSET)
    
    # Define train.txt e valid.txt: se SUBSET for "train", valid.txt ficará vazio e vice-versa.
    train_txt = subset_txt if SUBSET == "train" else ""
    criar_obj_data(archive_dir, num_classes, train_txt, backup_dir)
    
    criar_obj_names(archive_dir, CLASSES)
    
    print(f"Estrutura YOLO export criada em: {archive_dir}")

if __name__ == "__main__":
    main()

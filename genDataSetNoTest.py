import os
import random
import shutil

# Caminho para a pasta que contém suas imagens e labels
data_path = r'C:\Users\gustavonc\Downloads\imgs'

# Define os diretórios de treino e validação
train_images_dir = os.path.join('data/train/images')
train_labels_dir = os.path.join('data/train/labels')
valid_images_dir = os.path.join('data/valid/images')
valid_labels_dir = os.path.join('data/valid/labels')

# Cria os subdiretórios de treino e validação para imagens e labels
os.makedirs(train_images_dir, exist_ok=True)
os.makedirs(train_labels_dir, exist_ok=True)
os.makedirs(valid_images_dir, exist_ok=True)
os.makedirs(valid_labels_dir, exist_ok=True)

# Obtém todos os arquivos de imagem (ex.: .jpg, .png, etc.)
all_files = os.listdir(data_path)
image_files = [f for f in all_files if f.endswith('.jpg')]  # ajuste a extensão se necessário

# Define a proporção para treino e validação (ex.: 80% treino, 20% validação)
train_ratio = 0.8
valid_ratio = 0.2

# Aleatoriza a lista de arquivos de imagem
random.shuffle(image_files)

# Calcula quantos arquivos irão para treino e validação
train_size = int(len(image_files) * train_ratio)

# Divide os arquivos
train_files = image_files[:train_size]
valid_files = image_files[train_size:]

# Função para copiar as imagens e labels correspondentes para os diretórios adequados
def copy_files(file_list, src_dir, images_dest_dir, labels_dest_dir):
    for file_name in file_list:
        # Copiar arquivo de imagem
        shutil.copy(os.path.join(src_dir, file_name), os.path.join(images_dest_dir, file_name))

        # Copiar label correspondente (.txt) se existir
        label_file = file_name.replace('.jpg', '.txt')  # ajuste se necessário
        if os.path.exists(os.path.join(src_dir, label_file)):
            shutil.copy(os.path.join(src_dir, label_file), os.path.join(labels_dest_dir, label_file))

# Copia os arquivos para seus respectivos diretórios
copy_files(train_files, data_path, train_images_dir, train_labels_dir)
copy_files(valid_files, data_path, valid_images_dir, valid_labels_dir)

print('Arquivos copiados com sucesso!')

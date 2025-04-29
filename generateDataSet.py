import os
import random
import shutil

# Caminho para a pasta que contém suas imagens e labels
data_path = r'C:\Users\gustavonc\Downloads\AutoAnnotate\labels'

# Define os diretórios de treino, validação e teste
train_dir = r'C:\Users\gustavonc\Downloads\AutoAnnotate\yolo_dataset\train'
valid_dir = r'C:\Users\gustavonc\Downloads\AutoAnnotate\yolo_dataset\valid'
test_dir = r'C:\Users\gustavonc\Downloads\AutoAnnotate\yolo_datasetz\test'

# Cria os diretórios de treino, validação e teste se não existirem
os.makedirs(train_dir, exist_ok=True)
os.makedirs(valid_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# Obtém todos os arquivos de imagem (ex.: .jpg, .png, etc.)
all_files = os.listdir(data_path)
image_files = [f for f in all_files if f.endswith('.jpg')]  # ajuste a extensão se necessário

# Define a proporção para treino, validação e teste (ex.: 90% treino, 5% validação, 5% teste)
train_ratio = 0.9
valid_ratio = 0.05
test_ratio = 0.05

# Aleatoriza a lista de arquivos de imagem
random.shuffle(image_files)

# Calcula quantos arquivos irão para treino, validação e teste
train_size = int(len(image_files) * train_ratio)
valid_size = int(len(image_files) * valid_ratio)
test_size = len(image_files) - train_size - valid_size  # Restante para teste

# Divide os arquivos
train_files = image_files[:train_size]
valid_files = image_files[train_size:train_size + valid_size]
test_files = image_files[train_size + valid_size:]

# Função para mover as imagens e labels correspondentes
def move_files(file_list, src_dir, dest_dir):
    for file_name in file_list:
        # Mover arquivo de imagem
        shutil.move(os.path.join(src_dir, file_name), os.path.join(dest_dir, file_name))

        # Mover label correspondente (.txt) se existir
        label_file = file_name.replace('.jpg', '.txt')  # ajuste se necessário
        if os.path.exists(os.path.join(src_dir, label_file)):
            shutil.move(os.path.join(src_dir, label_file), os.path.join(dest_dir, label_file))

# Move os arquivos para seus respectivos diretórios
move_files(train_files, data_path, train_dir)
move_files(valid_files, data_path, valid_dir)
move_files(test_files, data_path, test_dir)

print('Arquivos movidos com sucesso!')

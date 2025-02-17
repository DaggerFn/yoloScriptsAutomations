import os

# Caminho para o diretório onde estão os arquivos de anotação
annotation_dir = r"C:\Users\gustavonc\Pictures\1- Treinamento YOLO WSFM\todos_postos\dataset_all_no_filter"

# Itera por todos os arquivos no diretório
for filename in os.listdir(annotation_dir):
    if filename.endswith(".txt"):
        file_path = os.path.join(annotation_dir, filename)
        
        # Lê o conteúdo do arquivo
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Escreve de volta com a correção
        with open(file_path, 'w') as file:
            for line in lines:
                parts = line.split()
                if parts:
                    # Corrige o ID da classe para inteiro
                    parts[0] = str(int(float(parts[0])))
                    file.write(" ".join(parts) + "\n")

print("Correção concluída!")

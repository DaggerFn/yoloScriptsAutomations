import cv2
import numpy as np
import argparse
import sys

class ROISelector:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.drawing = False
        self.start_x, self.start_y = -1, -1
        self.end_x, self.end_y = -1, -1
        self.result = None
        
        # Criar uma imagem preta do tamanho especificado
        self.image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Configurar a janela e o callback do mouse
        cv2.namedWindow('ROI Selector')
        cv2.setMouseCallback('ROI Selector', self.mouse_callback)
        
    def mouse_callback(self, event, x, y, flags, param):
        # Quando o botão do mouse é pressionado, começar a desenhar
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.start_x, self.start_y = x, y
            self.end_x, self.end_y = x, y
        
        # Enquanto o botão está pressionado e o mouse se move, atualizar o ponto final
        elif event == cv2.EVENT_MOUSEMOVE and self.drawing:
            # Criar uma cópia da imagem original
            temp_image = self.image.copy()
            self.end_x, self.end_y = x, y
            
            # Desenhar o retângulo na imagem temporária
            cv2.rectangle(temp_image, (self.start_x, self.start_y), (self.end_x, self.end_y), (0, 255, 0), 2)
            cv2.imshow('ROI Selector', temp_image)
        
        # Quando o botão do mouse é solto, parar de desenhar e capturar as coordenadas
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            self.end_x, self.end_y = x, y
            
            # Garantir que as coordenadas estejam dentro dos limites da imagem
            self.start_x = max(0, min(self.start_x, self.width - 1))
            self.start_y = max(0, min(self.start_y, self.height - 1))
            self.end_x = max(0, min(self.end_x, self.width - 1))
            self.end_y = max(0, min(self.end_y, self.height - 1))
            
            # Garantir que start_x/y seja o ponto superior esquerdo e end_x/y o ponto inferior direito
            x1 = min(self.start_x, self.end_x)
            y1 = min(self.start_y, self.end_y)
            x2 = max(self.start_x, self.end_x)
            y2 = max(self.start_y, self.end_y)
            
            # Criar o array de pontos no formato solicitado
            self.result = {
                'points': np.array([
                    [x1, y1],  # Superior esquerdo
                    [x2, y1],  # Superior direito
                    [x2, y2],  # Inferior direito
                    [x1, y2]   # Inferior esquerdo
                ], dtype=np.int32)
            }
            
            # Desenhar o retângulo final na imagem
            temp_image = self.image.copy()
            cv2.rectangle(temp_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.imshow('ROI Selector', temp_image)
    
    def run(self):
        print("Instruções:")
        print("1. Clique e arraste para desenhar um retângulo (ROI)")
        print("2. Solte o botão do mouse para finalizar a seleção")
        print("3. Pressione 'Enter' para confirmar ou 'Esc' para cancelar")
        
        # Loop principal
        while True:
            cv2.imshow('ROI Selector', self.image)
            key = cv2.waitKey(1) & 0xFF
            
            # Pressionar Enter confirma a seleção
            if key == 13:  # 13 é o código da tecla Enter
                if self.result is not None:
                    break
            # Pressionar Esc cancela a operação
            elif key == 27:  # 27 é o código da tecla Esc
                self.result = None
                break
        
        # Fechar a janela
        cv2.destroyAllWindows()
        return self.result


def get_resolution_from_args():
    parser = argparse.ArgumentParser(description='Selecionar ROI em uma imagem')
    parser.add_argument('--width', type=int, help='Largura da imagem')
    parser.add_argument('--height', type=int, help='Altura da imagem')
    args = parser.parse_args()
    
    # Se os argumentos não forem fornecidos pela linha de comando, solicitar ao usuário
    width = args.width
    height = args.height
    
    if width is None:
        try:
            width = int(input("Digite a largura da imagem: "))
        except ValueError:
            print("Largura inválida. Usando valor padrão de 480.")
            width = 480
    
    if height is None:
        try:
            height = int(input("Digite a altura da imagem: "))
        except ValueError:
            print("Altura inválida. Usando valor padrão de 320.")
            height = 320
    
    return width, height


def main():
    # Obter a resolução
    width, height = get_resolution_from_args()
    
    # Criar e executar o seletor de ROI
    roi_selector = ROISelector(width, height)
    result = roi_selector.run()
    
    # Exibir o resultado se uma ROI foi selecionada
    if result is not None:
        print(result)
    else:
        print("Operação cancelada pelo usuário.")


if __name__ == "__main__":
    main()
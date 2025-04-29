import cv2
import numpy as np
import argparse
import sys
import os

class ROISelector:
    def __init__(self, source=None, width=640, height=480, selection_mode="drag"):
        self.drawing = False
        self.start_x, self.start_y = -1, -1
        self.end_x, self.end_y = -1, -1
        self.result = None
        self.frame = None
        self.original_frame = None
        
        # Modo de seleção (drag ou points)
        self.selection_mode = selection_mode
        
        # Para modo de seleção por pontos
        self.points = []
        self.max_points = 4  # Número máximo de pontos (4 para um quadrilátero)
        
        # Verificar fonte da imagem
        if source is None or source == "":
            # Criar uma imagem preta do tamanho especificado se nenhuma fonte for fornecida
            self.cap = None
            self.width = width
            self.height = height
            self.image = np.zeros((height, width, 3), dtype=np.uint8)
            self.is_stream = False
        else:
            # Tentar abrir a fonte (arquivo de imagem, vídeo ou stream)
            if os.path.isfile(source):
                # Se for um arquivo de imagem
                self.image = cv2.imread(source)
                if self.image is None:
                    print(f"Erro ao carregar a imagem: {source}")
                    self.image = np.zeros((height, width, 3), dtype=np.uint8)
                else:
                    self.height, self.width = self.image.shape[:2]
                self.cap = None
                self.is_stream = False
            else:
                # Tentar abrir como stream ou vídeo
                try:
                    self.cap = cv2.VideoCapture(source)
                    if not self.cap.isOpened():
                        print(f"Erro ao abrir o stream: {source}")
                        self.cap = None
                        self.image = np.zeros((height, width, 3), dtype=np.uint8)
                        self.width = width
                        self.height = height
                        self.is_stream = False
                    else:
                        # Configurar as dimensões para o stream
                        ret, frame = self.cap.read()
                        if ret:
                            self.height, self.width = frame.shape[:2]
                            self.image = frame.copy()
                            self.original_frame = frame.copy()
                        else:
                            self.width = width
                            self.height = height
                            self.image = np.zeros((height, width, 3), dtype=np.uint8)
                        self.is_stream = True
                except Exception as e:
                    print(f"Erro ao abrir a fonte: {source}. Erro: {e}")
                    self.cap = None
                    self.image = np.zeros((height, width, 3), dtype=np.uint8)
                    self.width = width
                    self.height = height
                    self.is_stream = False
        
        # Configurar a janela e o callback do mouse
        cv2.namedWindow('ROI Selector')
        cv2.setMouseCallback('ROI Selector', self.mouse_callback)
        
    def mouse_callback(self, event, x, y, flags, param):
        # Modo de seleção por arrasto (drag)
        if self.selection_mode == "drag":
            # Quando o botão do mouse é pressionado, começar a desenhar
            if event == cv2.EVENT_LBUTTONDOWN:
                self.drawing = True
                self.start_x, self.start_y = x, y
                self.end_x, self.end_y = x, y
            
            # Enquanto o botão está pressionado e o mouse se move, atualizar o ponto final
            elif event == cv2.EVENT_MOUSEMOVE and self.drawing:
                # Se for stream, usar o frame atual, caso contrário, criar uma cópia da imagem
                if self.is_stream and self.original_frame is not None:
                    temp_image = self.original_frame.copy()
                else:
                    # Para imagens estáticas ou quando não há frame original
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
                if self.is_stream and self.original_frame is not None:
                    temp_image = self.original_frame.copy()
                else:
                    temp_image = self.image.copy()
                    
                cv2.rectangle(temp_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.imshow('ROI Selector', temp_image)
        
        # Modo de seleção por pontos
        elif self.selection_mode == "points":
            # Adicionar um ponto com clique do mouse
            if event == cv2.EVENT_LBUTTONDOWN:
                # Limitar o número de pontos
                if len(self.points) < self.max_points:
                    # Adicionar o ponto à lista
                    self.points.append((x, y))
                    
                    # Se for stream, usar o frame atual, caso contrário, criar uma cópia da imagem
                    if self.is_stream and self.original_frame is not None:
                        temp_image = self.original_frame.copy()
                    else:
                        # Para imagens estáticas ou quando não há frame original
                        temp_image = self.image.copy()
                    
                    # Desenhar todos os pontos atuais
                    for i, pt in enumerate(self.points):
                        cv2.circle(temp_image, pt, 5, (0, 0, 255), -1)
                        cv2.putText(temp_image, str(i+1), (pt[0]+10, pt[1]+10), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    
                    # Desenhar linhas entre os pontos
                    for i in range(len(self.points)):
                        if i < len(self.points) - 1:
                            cv2.line(temp_image, self.points[i], self.points[i+1], (255, 0, 0), 2)
                    
                    # Se tiver 4 pontos, fechar o polígono
                    if len(self.points) == self.max_points:
                        cv2.line(temp_image, self.points[0], self.points[3], (255, 0, 0), 2)
                        cv2.line(temp_image, self.points[1], self.points[2], (255, 0, 0), 2)
                        
                        # Reordenar os pontos para garantir que estejam no formato correto
                        # (superior esquerdo, superior direito, inferior direito, inferior esquerdo)
                        self.points = self.reorder_points(self.points)
                        
                        # Criar o array de pontos no formato solicitado
                        self.result = {
                            'points': np.array(self.points, dtype=np.int32)
                        }
                    
                    cv2.imshow('ROI Selector', temp_image)
    
    def reorder_points(self, points):
        """Reordena os pontos para garantir que estejam na ordem:
        [superior esquerdo, superior direito, inferior direito, inferior esquerdo]"""
        if len(points) != 4:
            return points
            
        # Converter para array numpy
        points_array = np.array(points)
        
        # Calcular o centro dos pontos
        center = np.mean(points_array, axis=0)
        
        # Classificar pontos por quadrante
        top_left = None
        top_right = None
        bottom_right = None
        bottom_left = None
        
        for pt in points:
            # Verificar posição em relação ao centro
            if pt[0] < center[0] and pt[1] < center[1]:
                top_left = pt
            elif pt[0] > center[0] and pt[1] < center[1]:
                top_right = pt
            elif pt[0] > center[0] and pt[1] > center[1]:
                bottom_right = pt
            elif pt[0] < center[0] and pt[1] > center[1]:
                bottom_left = pt
        
        # Se algum ponto não foi classificado, fazer uma classificação simples baseada em coordenadas
        if any(p is None for p in [top_left, top_right, bottom_right, bottom_left]):
            # Ordenar por coordenada y (obtém os dois pontos superiores e inferiores)
            sorted_by_y = sorted(points, key=lambda p: p[1])
            top_points = sorted_by_y[:2]
            bottom_points = sorted_by_y[2:]
            
            # Ordenar os pontos superiores pela coordenada x
            top_points = sorted(top_points, key=lambda p: p[0])
            top_left, top_right = top_points
            
            # Ordenar os pontos inferiores pela coordenada x
            bottom_points = sorted(bottom_points, key=lambda p: p[0])
            bottom_left, bottom_right = bottom_points
        
        return [top_left, top_right, bottom_right, bottom_left]
    
    def switch_selection_mode(self):
        """Alterna entre os modos de seleção"""
        if self.selection_mode == "drag":
            self.selection_mode = "points"
            self.points = []
            self.result = None
            print("Modo de seleção alterado para: Pontos")
        else:
            self.selection_mode = "drag"
            self.points = []
            self.result = None
            print("Modo de seleção alterado para: Arrasto")
    
    def run(self):
        print(f"\nModo de seleção atual: {'Arrasto' if self.selection_mode == 'drag' else 'Pontos'}")
        print("\nInstruções:")
        print("1. Selecione a ROI usando o método atual")
        print("2. Pressione 'Enter' para confirmar ou 'Esc' para cancelar")
        print("3. Pressione 'R' para reiniciar a seleção")
        print("4. Pressione 'M' para alternar entre os modos de seleção (arrasto/pontos)")
        
        if self.selection_mode == "drag":
            print("\nModo Arrasto: Clique e arraste para desenhar um retângulo")
        else:
            print("\nModo Pontos: Clique para adicionar cada ponto (máximo 4 pontos)")
        
        # Loop principal
        while True:
            # Atualizar o frame se for um stream
            if self.is_stream and self.cap is not None and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    self.original_frame = frame.copy()
                    self.image = frame.copy()
                    
                    # Se houver uma seleção em andamento, desenhe-a
                    if self.selection_mode == "drag":
                        if self.drawing:
                            # Durante o desenho
                            cv2.rectangle(self.image, (self.start_x, self.start_y), 
                                        (self.end_x, self.end_y), (0, 255, 0), 2)
                        elif self.result is not None:
                            # Depois que uma seleção foi feita
                            points = self.result['points']
                            x1, y1 = points[0]
                            x2, y2 = points[2]
                            cv2.rectangle(self.image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    elif self.selection_mode == "points":
                        # Desenhar todos os pontos selecionados
                        for i, pt in enumerate(self.points):
                            cv2.circle(self.image, pt, 5, (0, 0, 255), -1)
                            cv2.putText(self.image, str(i+1), (pt[0]+10, pt[1]+10), 
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        
                        # Desenhar linhas entre os pontos
                        for i in range(len(self.points)):
                            if i < len(self.points) - 1:
                                cv2.line(self.image, self.points[i], self.points[i+1], (255, 0, 0), 2)
                        
                        # Se tiver 4 pontos, fechar o polígono
                        if len(self.points) == self.max_points:
                            cv2.line(self.image, self.points[0], self.points[3], (255, 0, 0), 2)
                            cv2.line(self.image, self.points[1], self.points[2], (255, 0, 0), 2)
            
            # Exibir a imagem atual
            cv2.imshow('ROI Selector', self.image)
            key = cv2.waitKey(1) & 0xFF
            
            # Pressionar Enter confirma a seleção
            if key == 13:  # 13 é o código da tecla Enter
                if self.result is not None:
                    break
                elif self.selection_mode == "points" and len(self.points) == self.max_points:
                    # Reordenar os pontos e criar resultado
                    self.points = self.reorder_points(self.points)
                    self.result = {
                        'points': np.array(self.points, dtype=np.int32)
                    }
                    break
            # Pressionar Esc cancela a operação
            elif key == 27:  # 27 é o código da tecla Esc
                self.result = None
                break
            # Pressionar R reinicia a seleção
            elif key == ord('r'):
                self.result = None
                self.start_x, self.start_y = -1, -1
                self.end_x, self.end_y = -1, -1
                self.points = []
            # Pressionar M alterna o modo de seleção
            elif key == ord('m'):
                self.switch_selection_mode()
        
        # Fechar todos os recursos
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()
        return self.result


def parse_arguments():
    parser = argparse.ArgumentParser(description='Selecionar ROI em uma imagem ou stream')
    parser.add_argument('--source', type=str, help='Caminho para a imagem, vídeo ou URL do stream (ex: rtsp://...)')
    parser.add_argument('--width', type=int, default=640, help='Largura da imagem (usado apenas se nenhuma fonte for fornecida)')
    parser.add_argument('--height', type=int, default=480, help='Altura da imagem (usado apenas se nenhuma fonte for fornecida)')
    parser.add_argument('--mode', type=str, default='drag', choices=['drag', 'points'], 
                      help='Modo de seleção: drag (arrasto) ou points (pontos)')
    return parser.parse_args()


def main():
    # Obter argumentos da linha de comando
    args = parse_arguments()
    
    # Verificar se foi fornecida uma fonte
    source = args.source
    if source is None:
        # Perguntar ao usuário se ele deseja usar uma fonte específica
        use_source = input("Deseja carregar uma imagem ou stream? (s/n): ").lower()
        if use_source == 's' or use_source == 'sim':
            source_type = input("Digite o tipo (1: Imagem, 2: Stream RTSP, 3: Vídeo): ")
            
            if source_type == '1':
                source = input("Digite o caminho para a imagem: ")
            elif source_type == '2':
                source = input("Digite a URL do stream RTSP: ")
            elif source_type == '3':
                source = input("Digite o caminho para o vídeo: ")
            else:
                print("Tipo inválido. Usando imagem em branco.")
                source = None
    
    # Verificar o modo de seleção
    mode = args.mode
    if mode not in ["drag", "points"]:
        print("Modo inválido. Usando modo de arrasto (drag).")
        mode = "drag"
    
    # Criar e executar o seletor de ROI
    roi_selector = ROISelector(source=source, width=args.width, height=args.height, selection_mode=mode)
    result = roi_selector.run()
    
    # Exibir o resultado se uma ROI foi selecionada
    if result is not None:
        print(result)
    else:
        print("Operação cancelada pelo usuário.")


if __name__ == "__main__":
    main()
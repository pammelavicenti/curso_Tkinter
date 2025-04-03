import cv2
import numpy as np
import pyautogui

# Função para capturar coordenadas do mouse
def captura_coordenadas(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        img_copy = img.copy()
        cv2.putText(img_copy, f"X: {x} | Y: {y}", (x + 10, y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.imshow("Coordenadas da Tela", img_copy)

# Captura a tela
largura, altura = pyautogui.size()
img = np.zeros((altura, largura, 3), dtype=np.uint8)

cv2.namedWindow("Coordenadas da Tela", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("Coordenadas da Tela", captura_coordenadas)

while True:
    cv2.imshow("Coordenadas da Tela", img)
    if cv2.waitKey(1) & 0xFF == 27:  # Pressione 'Esc' para sair
        break

cv2.destroyAllWindows()

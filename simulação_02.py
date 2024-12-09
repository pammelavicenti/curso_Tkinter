import tkinter as tk
import random

# Variável para controlar o estado da esteira
running = True

# Função para mover os objetos na esteira
def move_belt():
    if running:
        for obj in objects:
            canvas.move(obj["id"], -5, 0)  # Move o objeto para a esquerda
            x1, y1, x2, y2 = canvas.coords(obj["id"])

            # Resetar a posição do objeto quando ele sai da tela
            if x2 < 0:
                canvas.move(obj["id"], 800 - x1, 0)  # Voltar para o início
                simulate_fault(obj)  # Simula uma falha no objeto

    # Continuar o loop de animação
    root.after(50, move_belt)

# Simula falhas nos objetos
def simulate_fault(obj):
    if random.random() < 0.2:  # 20% de chance de falha
        fault_type = random.choice(["rasgo", "furo"])
        if fault_type == "rasgo":
            canvas.itemconfig(obj["id"], fill="red")  # Cor vermelha indica rasgo
            log_event(f"Objeto {obj['id']}", "Rasgo Detectado")
        elif fault_type == "furo":
            canvas.itemconfig(obj["id"], fill="blue")  # Cor azul indica furo
            log_event(f"Objeto {obj['id']}", "Furo Detectado")
    else:
        canvas.itemconfig(obj["id"], fill="gray")  # Sem falhas

# Registra eventos no log
def log_event(obj_name, status):
    log_text.insert(tk.END, f"[Evento] {obj_name}: {status}\n")
    log_text.see(tk.END)  # Rola para o final do log

# Função para limpar o log
def clear_log():
    log_text.delete(1.0, tk.END)

# Função para ligar a esteira
def start_belt():
    global running
    running = True
    log_event("Sistema", "Esteira Ligada")

# Função para desligar a esteira
def stop_belt():
    global running
    running = False
    log_event("Sistema", "Esteira Desligada")

# Função para ativar o botão de emergência
def emergency_stop():
    global running
    running = False
    log_event("Emergência", "Esteira Parada Imediatamente")
    # Opcional: Indicar visualmente que a esteira parou
    for obj in objects:
        canvas.itemconfig(obj["id"], fill="yellow")

# Criando a janela principal
root = tk.Tk()
root.title("Simulação de Esteira Transportadora")
root.geometry("900x700")

# Criar o canvas para a esteira
canvas = tk.Canvas(root, width=800, height=300, bg="black")
canvas.pack(pady=20)

# Criar a "faixa" da esteira
canvas.create_rectangle(0, 140, 800, 160, fill="gray", outline="")

# Adicionar objetos na esteira
objects = []
for i in range(5):  # Criar 5 objetos
    obj_id = canvas.create_rectangle(50 + i * 150, 120, 100 + i * 150, 180, fill="gray")
    objects.append({"id": obj_id})

# Área de log para exibir os eventos
log_label = tk.Label(root, text="Log de Eventos:", font=("Helvetica", 14))
log_label.pack(pady=10)

log_text = tk.Text(root, height=10, width=80, font=("Helvetica", 12))
log_text.pack(pady=10)

# Botões de controle
control_frame = tk.Frame(root)
control_frame.pack(pady=20)

start_button = tk.Button(control_frame, text="Ligar Esteira", font=("Helvetica", 12), bg="green", fg="white", command=start_belt)
start_button.grid(row=0, column=0, padx=10)

stop_button = tk.Button(control_frame, text="Desligar Esteira", font=("Helvetica", 12), bg="red", fg="white", command=stop_belt)
stop_button.grid(row=0, column=1, padx=10)

emergency_button = tk.Button(control_frame, text="Botão de Emergência", font=("Helvetica", 12), bg="orange", fg="black", command=emergency_stop)
emergency_button.grid(row=0, column=2, padx=10)

# Botão para limpar o log
clear_log_button = tk.Button(root, text="Limpar Log", font=("Helvetica", 12), command=clear_log)
clear_log_button.pack(pady=10)

# Iniciar a animação da esteira
move_belt()

# Iniciar o loop da interface gráfica
root.mainloop()

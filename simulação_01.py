'''import tkinter as tk

# Função para ligar/desligar a correia
def toggle_belt():
    if belt_status_label.cget("text") == "Status: Desligada":
        belt_status_label.config(text="Status: Ligada", fg="green")
        toggle_button.config(text="Desligar Correia")
    else:
        belt_status_label.config(text="Status: Desligada", fg="red")
        toggle_button.config(text="Ligar Correia")

# Função para ajustar a velocidade da correia
def adjust_speed():
    speed_label.config(text=f"Velocidade: {speed_slider.get()} m/s")

# Criando a janela principal
root = tk.Tk()
root.title("Sistema Supervisório de Correia Transportadora")
root.geometry("500x400")

# Label para exibir o status da correia
belt_status_label = tk.Label(root, text="Status: Desligada", font=("Helvetica", 16), fg="red")
belt_status_label.pack(pady=20)

# Botão para ligar/desligar a correia
toggle_button = tk.Button(root, text="Ligar Correia", font=("Helvetica", 14), command=toggle_belt)
toggle_button.pack(pady=10)

# Label e slider para ajustar a velocidade da correia
speed_label = tk.Label(root, text="Velocidade: 0 m/s", font=("Helvetica", 14))
speed_label.pack(pady=10)

speed_slider = tk.Scale(root, from_=0, to=10, orient="horizontal", font=("Helvetica", 14), command=lambda val: adjust_speed())
speed_slider.pack(pady=10)

# Adicionar elementos adicionais (como temperatura ou sensores de carga)
temperature_label = tk.Label(root, text="Temperatura: 25°C", font=("Helvetica", 14))
temperature_label.pack(pady=10)

# Sensor de carga (exemplo simples)
load_sensor_label = tk.Label(root, text="Carga: 100 kg", font=("Helvetica", 14))
load_sensor_label.pack(pady=10)

# Iniciar o loop da interface gráfica
root.mainloop()'''


'''--------------------------------------'''



'''import tkinter as tk
from datetime import datetime

# Função para simular rasgo
def simulate_rasgo():
    rasgo_status.set(1 - rasgo_status.get())  # Alterna entre 0 (não detectado) e 1 (detectado)
    update_rasgo_status()
    log_event("Rasgo", "Detectado" if rasgo_status.get() else "Não Detectado")

# Função para simular furo
def simulate_furo():
    furo_status.set(1 - furo_status.get())  # Alterna entre 0 (não detectado) e 1 (detectado)
    update_furo_status()
    log_event("Furo", "Detectado" if furo_status.get() else "Não Detectado")

# Atualiza o status do rasgo
def update_rasgo_status():
    if rasgo_status.get() == 1:
        rasgo_label.config(text="Falha: Rasgo Detectado!", fg="red")
    else:
        rasgo_label.config(text="Rasgo Não Detectado", fg="green")

# Atualiza o status do furo
def update_furo_status():
    if furo_status.get() == 1:
        furo_label.config(text="Falha: Furo Detectado!", fg="red")
    else:
        furo_label.config(text="Furo Não Detectado", fg="green")

# Função para registrar eventos em um log
def log_event(tipo, status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_text.insert(tk.END, f"[{timestamp}] {tipo}: {status}\n")
    log_text.see(tk.END)  # Rola para o final do log

# Função para limpar o log
def clear_log():
    log_text.delete(1.0, tk.END)

# Criando a janela principal
root = tk.Tk()
root.title("Sistema de Detecção de Rasgos e Furos")
root.geometry("500x400")

# Indicadores de falha de Rasgo e Furo
rasgo_status = tk.IntVar(value=0)  # 0: não há falha, 1: falha de rasgo
furo_status = tk.IntVar(value=0)   # 0: não há falha, 1: falha de furo

rasgo_label = tk.Label(root, text="Rasgo Não Detectado", font=("Helvetica", 16), fg="green")
rasgo_label.pack(pady=20)

furo_label = tk.Label(root, text="Furo Não Detectado", font=("Helvetica", 16), fg="green")
furo_label.pack(pady=20)

# Botões para simular falhas
simulate_rasgo_button = tk.Button(root, text="Simular Rasgo", font=("Helvetica", 14), command=simulate_rasgo)
simulate_rasgo_button.pack(pady=10)

simulate_furo_button = tk.Button(root, text="Simular Furo", font=("Helvetica", 14), command=simulate_furo)
simulate_furo_button.pack(pady=10)

# Área de log para exibir os eventos
log_label = tk.Label(root, text="Log de Eventos:", font=("Helvetica", 14))
log_label.pack(pady=10)

log_text = tk.Text(root, height=10, width=50, font=("Helvetica", 12))
log_text.pack(pady=10)

# Botão para limpar o log
clear_log_button = tk.Button(root, text="Limpar Log", font=("Helvetica", 12), command=clear_log)
clear_log_button.pack(pady=5)

# Iniciar o loop da interface gráfica
root.mainloop() '''

'''----------------'''

'''
import tkinter as tk
from datetime import datetime
import random

# Função para atualizar os sensores com simulação
def simulate_sensors():
    # Simular valores de pressão ou vibração para rasgo
    simulated_pressure = random.randint(0, 100)  # Pressão simulada (0 a 100)
    pressure_label.config(text=f"Pressão: {simulated_pressure}")

    # Simular valores de deformação para furo
    simulated_deformation = random.randint(0, 100)  # Deformação simulada (0 a 100)
    deformation_label.config(text=f"Deformação: {simulated_deformation}")

    # Atualizar status do rasgo com base na pressão simulada
    if simulated_pressure > 80:  # Threshold de pressão
        if rasgo_status.get() == 0:
            rasgo_status.set(1)
            log_event("Rasgo", "Detectado")
    else:
        if rasgo_status.get() == 1:
            rasgo_status.set(0)
            log_event("Rasgo", "Resolvido")

    # Atualizar status do furo com base na deformação simulada
    if simulated_deformation > 70:  # Threshold de deformação
        if furo_status.get() == 0:
            furo_status.set(1)
            log_event("Furo", "Detectado")
    else:
        if furo_status.get() == 1:
            furo_status.set(0)
            log_event("Furo", "Resolvido")

    # Atualizar os indicadores
    update_rasgo_status()
    update_furo_status()

    # Agendar próxima simulação em 1 segundo
    root.after(1000, simulate_sensors)

# Atualiza o status do rasgo
def update_rasgo_status():
    if rasgo_status.get() == 1:
        rasgo_label.config(text="Falha: Rasgo Detectado!", fg="red")
    else:
        rasgo_label.config(text="Rasgo Não Detectado", fg="green")

# Atualiza o status do furo
def update_furo_status():
    if furo_status.get() == 1:
        furo_label.config(text="Falha: Furo Detectado!", fg="red")
    else:
        furo_label.config(text="Furo Não Detectado", fg="green")

# Função para registrar eventos em um log
def log_event(tipo, status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_text.insert(tk.END, f"[{timestamp}] {tipo}: {status}\n")
    log_text.see(tk.END)  # Rola para o final do log

# Função para limpar o log
def clear_log():
    log_text.delete(1.0, tk.END)

# Criando a janela principal
root = tk.Tk()
root.title("Sistema de Monitoramento - Simulação em Tempo Real")
root.geometry("500x500")

# Indicadores de falha de Rasgo e Furo
rasgo_status = tk.IntVar(value=0)  # 0: não há falha, 1: falha de rasgo
furo_status = tk.IntVar(value=0)   # 0: não há falha, 1: falha de furo

rasgo_label = tk.Label(root, text="Rasgo Não Detectado", font=("Helvetica", 16), fg="green")
rasgo_label.pack(pady=10)

furo_label = tk.Label(root, text="Furo Não Detectado", font=("Helvetica", 16), fg="green")
furo_label.pack(pady=10)

# Labels para exibir valores simulados
pressure_label = tk.Label(root, text="Pressão: 0", font=("Helvetica", 14))
pressure_label.pack(pady=10)

deformation_label = tk.Label(root, text="Deformação: 0", font=("Helvetica", 14))
deformation_label.pack(pady=10)

# Área de log para exibir os eventos
log_label = tk.Label(root, text="Log de Eventos:", font=("Helvetica", 14))
log_label.pack(pady=10)

log_text = tk.Text(root, height=10, width=50, font=("Helvetica", 12))
log_text.pack(pady=10)

# Botão para limpar o log
clear_log_button = tk.Button(root, text="Limpar Log", font=("Helvetica", 12), command=clear_log)
clear_log_button.pack(pady=5)

# Iniciar a simulação automática
simulate_sensors()

# Iniciar o loop da interface gráfica
root.mainloop()'''

import tkinter as tk
import random

# Função para mover os objetos na esteira
def move_belt():
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

# Criando a janela principal
root = tk.Tk()
root.title("Simulação de Esteira Transportadora")
root.geometry("900x600")

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

# Botão para limpar o log
clear_log_button = tk.Button(root, text="Limpar Log", font=("Helvetica", 12), command=clear_log)
clear_log_button.pack(pady=5)

# Iniciar a animação da esteira
move_belt()

# Iniciar o loop da interface gráfica
root.mainloop()



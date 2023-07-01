import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import paramiko

def aplicar_configuracion():
    # Obtener los valores de host, usuario, contraseña y puerto SSH
    host = host_entry.get() if not host_file else ""
    usuario = usuario_entry.get()
    contrasena = contrasena_entry.get()
    puerto_ssh = int(puerto_ssh_entry.get())

    # Obtener la configuración de la CLI del MikroTik
    configuracion = cli_textbox.get("1.0", tk.END)

    # Mostrar mensaje de estado en el campo de texto resultado_label
    resultado_label.configure(text="Realizando configuración, favor espere...")

    try:
        # Si se seleccionó un archivo de hosts, leer los hosts desde el archivo
        if host_file:
            with open(host_file, "r") as file:
                hosts = file.read().splitlines()
        else:
            # Si no se seleccionó un archivo, utilizar el host ingresado en el campo
            hosts = [host]

        total_hosts = len(hosts)
        progreso = 0

        for h in hosts:
            # Establecer la conexión SSH con el MikroTik
            cliente_ssh = paramiko.SSHClient()
            cliente_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            cliente_ssh.connect(hostname=h, port=puerto_ssh, username=usuario, password=contrasena)

            # Ejecutar los comandos de configuración en el MikroTik
            stdin, stdout, stderr = cliente_ssh.exec_command(configuracion)

            # Obtener el resultado de la ejecución de los comandos
            resultado = stdout.read().decode()

            # Mostrar el resultado en el campo de texto resultado_label
            resultado_label.configure(text="Configuración Exitosa", fg="green")

            # Cerrar la conexión SSH
            cliente_ssh.close()

            progreso += 1
            progreso_porcentaje = int(progreso / total_hosts * 100)
            progreso_label.configure(text="Progreso: {}%".format(progreso_porcentaje))

        # Limpiar los campos de entrada después de aplicar la configuración
        host_entry.delete(0, tk.END)
        usuario_entry.delete(0, tk.END)
        contrasena_entry.delete(0, tk.END)
        puerto_ssh_entry.delete(0, tk.END)
        cli_textbox.delete("1.0", tk.END)
        resultado_label.configure(text="")

    except Exception as e:
        # Mostrar el mensaje de error en el campo de texto resultado_label
        resultado_label.configure(text="La configuración no ha podido ser aplicada, inténtelo nuevamente.")
        print(e)

def seleccionar_archivo_hosts():
    global host_file
    host_file = filedialog.askopenfilename(initialdir="/", title="Seleccionar archivo", filetypes=(("Archivos de texto", "*.txt"),))

    if host_file:
        host_entry.delete(0, tk.END)
        host_entry.insert(tk.END, host_file)

def limpiar_memoria():
    global host_file
    host_file = None

# Crear la ventana principal
ventana = ctk.CTkWindow()
ventana.title("MikroFlow 1.0")
ventana.geometry("655x540")
ventana.resizable(False, False)

# Crear el frame principal
frame_principal = ctk.CTkFrame(ventana, height=650, width=530)
frame_principal.pack(pady=20)

# Estilo de los inputs
entry_style = {"font": ("Arial", 12), "width": 20, "highlightthickness": 0, "bg": "#333333", "fg": "white"}

# Crear los widgets necesarios
host_label = ctk.CTkLabel(frame_principal, text="Host:")
host_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
host_entry = ctk.CTkEntry(frame_principal)
host_entry.grid(row=0, column=1, padx=(10, 5), pady=5)

seleccionar_archivo_button = ctk.CTkButton(frame_principal, text="Seleccionar archivo", command=seleccionar_archivo_hosts)
seleccionar_archivo_button.grid(row=0, column=2, padx=(0, 10), pady=5, sticky="e")

usuario_label = ctk.CTkLabel(frame_principal, text="Usuario:")
usuario_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
usuario_entry = ctk.CTkEntry(frame_principal)
usuario_entry.grid(row=1, column=1, padx=10, pady=5)

contrasena_label = ctk.CTkLabel(frame_principal, text="Contraseña:")
contrasena_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
contrasena_entry = ctk.CTkEntry(frame_principal, show="*")
contrasena_entry.grid(row=2, column=1, padx=10, pady=5)

puerto_ssh_label = ctk.CTkLabel(frame_principal, text="Puerto SSH:")
puerto_ssh_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
puerto_ssh_entry = ctk.CTkEntry(frame_principal)
puerto_ssh_entry.grid(row=3, column=1, padx=10, pady=5)

cli_label = ctk.CTkLabel(frame_principal, text="Comandos de Configuración:")
cli_label.grid(row=4, column=0, sticky="w", padx=10, pady=10)
cli_textbox = ctk.CTkTextbox(frame_principal, width=80, height=15)
cli_textbox.grid(row=5, column=0, columnspan=3, padx=10, pady=5)

# Resultado
resultado_label = ctk.CTkLabel(frame_principal, text="Resultado:")
resultado_label.grid(row=4, column=1, sticky="w", padx=10, pady=10)
resultado_label_result = ctk.CTkLabel(frame_principal, text="")
resultado_label_result.grid(row=5, column=1, padx=10, pady=5, sticky="w")

# Etiqueta de porcentaje de progreso
progreso_label = ctk.CTkLabel(frame_principal, text="Progreso: 0%")
progreso_label.grid(row=6, column=0, sticky="w", padx=10, pady=10)

# Botones
aplicar_button = ctk.CTkButton(frame_principal, text="Aplicar Configuración", command=aplicar_configuracion)
aplicar_button.grid(row=6, column=1, padx=(0, 10), pady=10, sticky="e")

limpiar_button = ctk.CTkButton(frame_principal, text="Limpiar", command=limpiar_memoria)
limpiar_button.grid(row=6, column=2, padx=(0, 10), pady=10, sticky="e")

# Ejecutar la ventana principal
ventana.mainloop()


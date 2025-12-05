import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time
from datetime import datetime, timedelta
import os

class FullScreenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GONAHyallowance")
        
        # Configurar ventana para pantalla completa
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')
        
        # Crear frame principal con fondo negro
        main_frame = tk.Frame(root, bg='black')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)
        
        # Crear marco principal con borde rojo grueso
        self.main_border = tk.Frame(main_frame, bg='red', bd=5, relief='solid')
        self.main_border.pack(fill=tk.BOTH, expand=True)
        
        # Frame interior con fondo negro
        self.content_frame = tk.Frame(self.main_border, bg='black')
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        
        # Cargar y mostrar imagen del jester
        self.load_jester_image()
        
        # Separador rojo después de la imagen
        separator1 = tk.Frame(self.content_frame, height=3, bg='red')
        separator1.pack(fill=tk.X, padx=20, pady=10)
        
        # Mostrar texto
        self.display_text()
        
        # Separador rojo antes del contador
        separator2 = tk.Frame(self.content_frame, height=3, bg='red')
        separator2.pack(fill=tk.X, padx=20, pady=10)
        
        # Configurar contador con 500 horas
        self.end_time = datetime.now() + timedelta(hours=500)
        
        # Marco rojo alrededor del contador
        time_border = tk.Frame(self.content_frame, bg='red', bd=3, relief='solid')
        time_border.pack(pady=20, padx=100)
        
        self.time_label = tk.Label(time_border, text="", font=('Courier', 20, 'bold'), 
                                  fg='red', bg='black', padx=20, pady=10)
        self.time_label.pack()
        
        self.update_timer()
        
        # Botón para salir (presionar ESC)
        self.root.bind('<Escape>', lambda e: root.destroy())
        
        # Botón para salir (también con clic)
        exit_btn = tk.Button(self.content_frame, text="SALIR (ESC)", font=('Courier', 10, 'bold'),
                           fg='white', bg='red', command=root.destroy)
        exit_btn.pack(pady=10)

    def load_jester_image(self):
        try:
            # Cargar imagen
            image = Image.open("jester.png")
            
            # Redimensionar para que quepa en el cuadro
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # Calcular tamaño máximo para la imagen (60% del alto de la pantalla)
            max_height = int(screen_height * 0.4)
            width_percent = max_height / float(image.size[1])
            target_width = int((float(image.size[0]) * float(width_percent)))
            
            # Ajustar si es muy ancha
            if target_width > screen_width * 0.8:
                target_width = int(screen_width * 0.8)
                height_percent = target_width / float(image.size[0])
                max_height = int((float(image.size[1]) * float(height_percent)))
            
            image = image.resize((target_width, max_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            # Marco rojo alrededor de la imagen
            image_border = tk.Frame(self.content_frame, bg='red', bd=3, relief='solid')
            image_border.pack(pady=20, padx=50)
            
            # Mostrar imagen
            image_label = tk.Label(image_border, image=photo, bg='black')
            image_label.image = photo  # Guardar referencia
            image_label.pack(padx=3, pady=3)
            
        except Exception as e:
            # Si no encuentra la imagen, mostrar mensaje en marco rojo
            error_border = tk.Frame(self.content_frame, bg='red', bd=3, relief='solid')
            error_border.pack(pady=20, padx=50)
            
            error_label = tk.Label(error_border, text="jester.png no encontrado\nColoca la imagen en la misma carpeta", 
                                 font=('Courier', 12, 'bold'), fg='red', bg='black', padx=20, pady=20)
            error_label.pack()

    def display_text(self):
        text_content = [
            ("# GONAHyallowance", 'red', 18, 'bold'),
            ("Your hire are encrypted.", 'white', 12, 'normal'),
            ("", 'white', 12, 'normal'),
            ("To get the key to decrypt files, you have access 0.9 million USD", 'white', 12, 'normal'),
            ("of payment is not made by transmission only, and this is your entire system.", 'white', 12, 'normal'),
            ("", 'white', 12, 'normal'),
            ("More instructions forthcoming – funding.", 'yellow', 12, 'bold'),
            ("", 'white', 12, 'normal'),
            ("How options must find content?", 'white', 12, 'normal'),
            ("12/23/14/22:00", 'yellow', 14, 'bold'),
            ("", 'white', 12, 'normal'),
            ("Total occupied 4,125 encrypted files.", 'white', 12, 'normal'),
            ("", 'white', 12, 'normal'),
            ("─" * 60, 'red', 12, 'bold'),
            ("", 'white', 12, 'normal'),
            ("UNION UNION UNION UNION UNION UNION", 'red', 16, 'bold'),
            ("", 'white', 12, 'normal'),
            ("─" * 60, 'red', 12, 'bold'),
            ("", 'white', 12, 'normal'),
            ("JUST TO GO ACTIVAL", 'yellow', 14, 'bold'),
            ("Thisty's all overhead element of goods and fuel in most things.", 'white', 12, 'normal'),
            ("The first is its space that costs well out membership.", 'white', 12, 'normal')
        ]
        
        for line, color, size, weight in text_content:
            if line.startswith("─"):
                # Línea separadora roja
                sep_frame = tk.Frame(self.content_frame, height=2, bg='red')
                sep_frame.pack(fill=tk.X, padx=30, pady=5)
            elif line == "":
                # Espacio vacío
                spacer = tk.Label(self.content_frame, text=" ", font=('Courier', 4), 
                                fg='black', bg='black')
                spacer.pack()
            else:
                label = tk.Label(self.content_frame, text=line, 
                               font=('Courier', size, weight), 
                               fg=color, bg='black')
                label.pack(pady=1)

    def update_timer(self):
        current_time = datetime.now()
        time_left = self.end_time - current_time
        
        if time_left.total_seconds() <= 0:
            self.time_label.config(text="TIME EXPIRED", fg='red')
            return
        
        hours = int(time_left.total_seconds() // 3600)
        minutes = int((time_left.total_seconds() % 3600) // 60)
        seconds = int(time_left.total_seconds() % 60)
        
        time_text = f"Time left: {hours:03d}h {minutes:02d}m {seconds:02d}s"
        self.time_label.config(text=time_text, fg='red')
        
        # Actualizar cada segundo
        self.root.after(1000, self.update_timer)

if __name__ == "__main__":
    root = tk.Tk()
    app = FullScreenApp(root)
    root.mainloop()
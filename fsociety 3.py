import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import time
from datetime import datetime, timedelta
import ctypes
import sys

class SafeRansomwareSimulator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FSociety")
        
        # Ocultar barra de tareas y hacer pantalla completa
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='#0c0c0c')
        self.root.bind('<Escape>', self.attempt_exit)
        
        # Intentar ocultar la barra de tareas
        self.hide_taskbar()
        
        # Configurar tiempo de expiración
        self.expire_time = datetime.now() + timedelta(hours=14, minutes=4, seconds=8)
        self.exit_attempts = 0
        self.exit_password = "123"
        self.taskbar_visible = False
        
        self.setup_ui()
    
    def hide_taskbar(self):
        """Intenta ocultar la barra de tareas"""
        try:
            # Para Windows
            if os.name == 'nt':
                # Ocultar la barra de tareas
                hwnd = ctypes.windll.user32.FindWindowW("Shell_traywnd", None)
                ctypes.windll.user32.ShowWindow(hwnd, 0)
                self.taskbar_visible = False
        except:
            pass
    
    def show_taskbar(self):
        """Muestra la barra de tareas nuevamente"""
        try:
            # Para Windows
            if os.name == 'nt':
                hwnd = ctypes.windll.user32.FindWindowW("Shell_traywnd", None)
                ctypes.windll.user32.ShowWindow(hwnd, 1)
                self.taskbar_visible = True
        except:
            pass
    
    def setup_ui(self):
        # Frame principal centrado
        main_frame = tk.Frame(self.root, bg='#0c0c0c')
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Título principal
        title_label = tk.Label(
            main_frame,
            text="#OPdailyallowance",
            font=("Courier", 20, "bold"),
            fg="#00ff00",
            bg='#0c0c0c'
        )
        title_label.pack(pady=(0, 20))
        
        # Mensaje de advertencia
        warning_text = tk.Label(
            main_frame,
            text="Your files are encrypted.",
            font=("Arial", 16, "bold"),
            fg="#ff0000",
            bg='#0c0c0c'
        )
        warning_text.pack(pady=(0, 15))
        
        # Texto descriptivo
        desc_text = """To get the key to decrypt files, you have to paid 5.9 million USD. 
If payment is not made by tomorrow night we'll brick your entire system.

More instructions forthcoming - fsociety"""
        
        desc_label = tk.Label(
            main_frame,
            text=desc_text,
            font=("Arial", 12),
            fg="#ffffff",
            bg='#0c0c0c',
            justify='left'
        )
        desc_label.pack(pady=(0, 25))
        
        # Frame de información del sistema
        info_frame = tk.Frame(main_frame, bg='#1a1a1a', padx=20, pady=10)
        info_frame.pack(fill='x', pady=(0, 25))
        
        # Tiempo restante
        self.time_label = tk.Label(
            info_frame,
            text=f"Time left: 14h 04m 08s",
            font=("Courier", 14, "bold"),
            fg="#ffff00",
            bg='#1a1a1a'
        )
        self.time_label.pack(pady=5)
        
        # Información del sistema
        system_info = tk.Label(
            info_frame,
            text="Your system: (064)\nFirst connect IP: 192.251.68.260\nTotal encrypted: 5,326 encrypted files",
            font=("Courier", 11),
            fg="#cccccc",
            bg='#1a1a1a',
            justify='left'
        )
        system_info.pack(pady=5)
        
        # Barra de navegación
        nav_frame = tk.Frame(main_frame, bg='#0c0c0c')
        nav_frame.pack(fill='x', pady=(0, 25))
        
        nav_buttons = ["Edresh", "Payment", "FAQ", "Decrypt first file for FREE", "Support"]
        
        for i, button_text in enumerate(nav_buttons):
            btn = tk.Button(
                nav_frame,
                text=button_text,
                font=("Arial", 10),
                fg="#00ff00",
                bg="#1a1a1a",
                relief='flat',
                borderwidth=1,
                padx=15,
                pady=8,
                command=lambda bt=button_text: self.nav_button_click(bt)
            )
            btn.pack(side='left', padx=8)
        
        # Separador
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill='x', pady=25)
        
        # Imagen Jester
        self.load_jester_image(main_frame)
        
        # Cita de Jester
        quote_text = """There's an unequal amount of good and bad in most things. 
The trick is to figure out the ratio and act accordingly."""
        
        quote_label = tk.Label(
            main_frame,
            text=quote_text,
            font=("Arial", 11, "italic"),
            fg="#888888",
            bg='#0c0c0c',
            justify='center'
        )
        quote_label.pack(pady=20)
        
        # Mensaje de instrucciones para salir
        exit_instruction = tk.Label(
            main_frame,
            text="Press ESC to attempt exit (Password required)",
            font=("Arial", 10),
            fg="#ff4444",
            bg='#0c0c0c'
        )
        exit_instruction.pack(pady=10)
        
        # Actualizar contador de tiempo
        self.update_timer()
    
    def load_jester_image(self, parent):
        try:
            # Intentar cargar la imagen jester.png
            if os.path.exists("jester.png"):
                image = Image.open("jester.png")
                # Redimensionar para pantalla completa
                if image.width > 500 or image.height > 350:
                    image = image.resize((500, 350), Image.Resampling.LANCZOS)
                
                photo = ImageTk.PhotoImage(image)
                
                image_label = tk.Label(
                    parent,
                    image=photo,
                    bg='#0c0c0c'
                )
                image_label.image = photo
                image_label.pack(pady=20)
            else:
                # Si no existe la imagen, mostrar placeholder
                placeholder = tk.Label(
                    parent,
                    text="[JESTER IMAGE - jester.png not found]",
                    font=("Arial", 14),
                    fg="#ff0000",
                    bg='#0c0c0c'
                )
                placeholder.pack(pady=20)
                
        except Exception as e:
            error_label = tk.Label(
                parent,
                text=f"[Error loading image: {str(e)}]",
                font=("Arial", 12),
                fg="#ff0000",
                bg='#0c0c0c'
            )
            error_label.pack(pady=20)
    
    def update_timer(self):
        """Actualiza el contador de tiempo (simulado)"""
        current_time = datetime.now()
        time_left = self.expire_time - current_time
        
        if time_left.total_seconds() > 0:
            hours = int(time_left.total_seconds() // 3600)
            minutes = int((time_left.total_seconds() % 3600) // 60)
            seconds = int(time_left.total_seconds() % 60)
            
            time_text = f"Time left: {hours:02d}h {minutes:02d}m {seconds:02d}s"
            self.time_label.config(text=time_text)
            
            # Actualizar cada segundo
            self.root.after(1000, self.update_timer)
        else:
            self.time_label.config(text="Time left: EXPIRED", fg="#ff0000")
    
    def nav_button_click(self, button_text):
        """Maneja los clics en los botones de navegación"""
        messagebox.showinfo(
            "Simulation Info", 
            f"Button '{button_text}' clicked.\n\nThis is a simulation - no real action will be taken."
        )
    
    def attempt_exit(self, event=None):
        """Intenta salir de la aplicación con contraseña"""
        self.exit_attempts += 1
        
        if self.exit_attempts == 1:
            messagebox.showwarning(
                "Exit Attempt",
                "You cannot exit without the password!\n\n"
                "Press ESC again and enter the password to exit."
            )
        else:
            password = self.ask_password()
            if password == self.exit_password:
                # Restaurar barra de tareas antes de salir
                self.show_taskbar()
                if messagebox.askyesno(
                    "Confirm Exit", 
                    "Password accepted!\n\nThis is a safe simulation. No files have been encrypted.\n\nClose application?"
                ):
                    self.root.destroy()
            else:
                messagebox.showerror(
                    "Access Denied",
                    "Incorrect password!\n\nYou cannot exit without the correct password."
                )
                self.exit_attempts = 0  # Reset attempts
    
    def ask_password(self):
        """Dialogo para pedir contraseña"""
        password_window = tk.Toplevel(self.root)
        password_window.title("Password Required")
        password_window.geometry("300x150")
        password_window.configure(bg='#0c0c0c')
        password_window.attributes('-topmost', True)
        
        # Centrar la ventana de contraseña
        password_window.transient(self.root)
        password_window.grab_set()
        
        tk.Label(
            password_window,
            text="Enter password to exit:",
            font=("Arial", 12),
            fg="#ffffff",
            bg='#0c0c0c'
        ).pack(pady=15)
        
        password_var = tk.StringVar()
        password_entry = tk.Entry(
            password_window,
            textvariable=password_var,
            show="*",
            font=("Arial", 12),
            width=20
        )
        password_entry.pack(pady=10)
        password_entry.focus()
        
        result = {"password": ""}
        
        def submit_password():
            result["password"] = password_var.get()
            password_window.destroy()
        
        tk.Button(
            password_window,
            text="Submit",
            command=submit_password,
            font=("Arial", 10),
            bg="#00ff00",
            fg="#000000"
        ).pack(pady=10)
        
        password_window.bind('<Return>', lambda e: submit_password())
        
        # Esperar hasta que la ventana se cierre
        password_entry.focus_set()
        self.root.wait_window(password_window)
        
        return result["password"]
    
    def on_closing(self):
        """Maneja el intento de cierre con la X"""
        self.attempt_exit()

def main():
    # Ejecutar la simulación directamente sin advertencias
    app = SafeRansomwareSimulator()
    
    # Manejar el cierre de la ventana
    app.root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    app.root.mainloop()
    
    # Asegurarse de que la barra de tareas se restaure al salir
    try:
        if os.name == 'nt':
            hwnd = ctypes.windll.user32.FindWindowW("Shell_traywnd", None)
            ctypes.windll.user32.ShowWindow(hwnd, 1)
    except:
        pass

if __name__ == "__main__":
    main()
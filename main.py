#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicación principal del sistema de gestión de agua potable
"""

import tkinter as tk
from tkinter import messagebox, ttk
import os
from PIL import Image, ImageTk
from auth import authenticate
from user_management import UserManagementWindow
from payment_registration import PaymentRegistrationWindow
from configuration import ConfigurationWindow

class MainApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("💧 Sistema de Gestión de Agua Potable - Versión Profesional")
        self.root.geometry("900x650")
        self.root.resizable(True, True)
        
        # Colores mejorados pero compatibles
        self.colors = {
            'primary': '#2980b9',      # Azul profesional
            'secondary': '#3498db',    # Azul claro
            'success': '#27ae60',      # Verde
            'warning': '#f39c12',      # Naranja
            'danger': '#e74c3c',       # Rojo
            'dark': '#2c3e50',         # Azul oscuro
            'light': '#ecf0f1',        # Gris claro
            'white': '#ffffff'         # Blanco
        }
        
        # Configurar el icono de la ventana (si existe)
        self.set_window_icon()
        
        # Centrar la ventana
        self.center_window()
        
        # Variables
        self.logo_image = None
        self.example_image = None
        
        # Configurar la interfaz mejorada
        self.setup_improved_ui()
        
        # Configurar eventos
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_improved_menu(self):
        """Crea la barra de menú mejorada"""
        menubar = tk.Menu(self.root, 
                         bg=self.colors['white'], 
                         fg=self.colors['dark'],
                         activebackground=self.colors['primary'],
                         activeforeground=self.colors['white'],
                         font=('Segoe UI', 9))
        self.root.config(menu=menubar)
        
        # Menú Sistema con mejor diseño
        system_menu = tk.Menu(menubar, tearoff=0,
                             bg=self.colors['white'],
                             fg=self.colors['dark'],
                             activebackground=self.colors['primary'],
                             activeforeground=self.colors['white'])
        menubar.add_cascade(label="🏠 Sistema", menu=system_menu)
        system_menu.add_command(label="🏠 Menú Principal", command=self.show_main_window)
        system_menu.add_separator()
        system_menu.add_command(label="📊 Importar CSV", command=self.open_csv_importer)
        system_menu.add_separator()
        system_menu.add_command(label="🚪 Salir", command=self.on_closing)
        
        # Menú Módulos
        modules_menu = tk.Menu(menubar, tearoff=0,
                              bg=self.colors['white'],
                              fg=self.colors['dark'],
                              activebackground=self.colors['primary'],
                              activeforeground=self.colors['white'])
        menubar.add_cascade(label="⚙️ Módulos", menu=modules_menu)
        modules_menu.add_command(label="👥 Gestión de Usuarios", command=self.open_user_management)
        modules_menu.add_command(label="💰 Registro de Pagos", command=self.open_payment_registration)
        modules_menu.add_command(label="⚙️ Configuración del Sistema", command=self.open_configuration)
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0,
                           bg=self.colors['white'],
                           fg=self.colors['dark'],
                           activebackground=self.colors['primary'],
                           activeforeground=self.colors['white'])
        menubar.add_cascade(label="❓ Ayuda", menu=help_menu)
        help_menu.add_command(label="📖 Instrucciones de Uso", command=self.show_instructions)
        help_menu.add_command(label="ℹ️ Acerca del Sistema", command=self.show_about)
    
    def set_window_icon(self):
        """Configura el icono de la ventana si existe"""
        try:
            if os.path.exists("logo.jpg"):
                # Convertir JPG a ICO si es necesario
                img = Image.open("logo.jpg")
                img = img.resize((32, 32), Image.Resampling.LANCZOS)
                # En Windows, podemos usar el archivo directamente
                # self.root.iconbitmap("logo.ico")  # Si tuviéramos un ICO
        except Exception as e:
            print(f"No se pudo configurar el icono: {e}")
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_improved_ui(self):
        """Configura la interfaz de usuario mejorada"""
        # Configurar el fondo principal
        self.root.configure(bg=self.colors['light'])
        
        # Crear menú mejorado
        self.create_improved_menu()
        
        # Frame principal con mejor diseño
        main_frame = tk.Frame(self.root, bg=self.colors['light'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header profesional con logo destacado
        self.create_professional_header(main_frame)
        
        # Área central con módulos mejorados
        self.create_improved_modules_area(main_frame)
        
        # Footer elegante
        self.create_elegant_footer(main_frame)
    
    def create_professional_header(self, parent):
        """Crea el encabezado profesional mejorado"""
        # Header con diseño elegante
        header_frame = tk.Frame(parent, bg=self.colors['dark'], height=140)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Línea decorativa superior
        top_line = tk.Frame(header_frame, bg=self.colors['primary'], height=4)
        top_line.pack(fill=tk.X)
        
        # Contenido del header
        content_frame = tk.Frame(header_frame, bg=self.colors['dark'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)
        
        # Panel izquierdo - Logo destacado
        left_panel = tk.Frame(content_frame, bg=self.colors['dark'])
        left_panel.pack(side=tk.LEFT, fill=tk.Y)
        
        # Cargar y mostrar logo con mejor presentación
        if os.path.exists("logo.jpg"):
            try:
                logo_img = Image.open("logo.jpg")
                # Logo más grande y visible
                logo_img = logo_img.resize((100, 100), Image.Resampling.LANCZOS)
                self.logo_image = ImageTk.PhotoImage(logo_img)
                
                # Frame para el logo con borde elegante
                logo_container = tk.Frame(left_panel, bg=self.colors['white'], relief='solid', bd=2)
                logo_container.pack(padx=(0, 25), pady=5)
                
                logo_label = tk.Label(
                    logo_container,
                    image=self.logo_image,
                    bg=self.colors['white']
                )
                logo_label.pack(padx=5, pady=5)
                
            except Exception as e:
                print(f"Error al cargar logo: {e}")
                # Logo por defecto si no se puede cargar
                default_logo = tk.Label(
                    left_panel,
                    text="💧\nLOGO",
                    font=('Segoe UI', 16, 'bold'),
                    fg=self.colors['primary'],
                    bg=self.colors['dark'],
                    justify=tk.CENTER
                )
                default_logo.pack(padx=(0, 25))
        
        # Panel derecho - Información de la empresa
        right_panel = tk.Frame(content_frame, bg=self.colors['dark'])
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Título principal más prominente
        title_label = tk.Label(
            right_panel,
            text="💧 SISTEMA DE GESTIÓN DE AGUA POTABLE",
            font=('Segoe UI', 18, 'bold'),
            fg=self.colors['white'],
            bg=self.colors['dark']
        )
        title_label.pack(anchor='w', pady=(5, 0))
        
        # Subtítulo de la empresa
        company_label = tk.Label(
            right_panel,
            text="🏢 COMITÉ DE AGUA POTABLE - GESTIÓN PROFESIONAL",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['secondary'],
            bg=self.colors['dark']
        )
        company_label.pack(anchor='w', pady=(5, 0))
        
        # Línea separadora
        separator = tk.Frame(right_panel, bg=self.colors['primary'], height=2)
        separator.pack(fill=tk.X, pady=(8, 8))
        
        # Información adicional
        info_label = tk.Label(
            right_panel,
            text="✨ Versión Profesional 2.0 | 🐍 Powered by Python",
            font=('Segoe UI', 10),
            fg='#bdc3c7',
            bg=self.colors['dark']
        )
        info_label.pack(anchor='w')
        
        # Status de conexión
        status_label = tk.Label(
            right_panel,
            text="🟢 Sistema Activo • Base de Datos Conectada",
            font=('Segoe UI', 9, 'bold'),
            fg=self.colors['success'],
            bg=self.colors['dark']
        )
        status_label.pack(anchor='w', pady=(5, 0))
    
    def create_improved_modules_area(self, parent):
        """Crea el área central con módulos mejorados"""
        modules_frame = tk.Frame(parent, bg=self.colors['light'])
        modules_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=25)
        
        # Título de la sección más elegante
        title_container = tk.Frame(modules_frame, bg=self.colors['white'], relief='solid', bd=1)
        title_container.pack(fill=tk.X, pady=(0, 25))
        
        section_title = tk.Label(
            title_container,
            text="🎯 MÓDULOS DEL SISTEMA PROFESIONAL",
            font=('Segoe UI', 16, 'bold'),
            fg=self.colors['dark'],
            bg=self.colors['white']
        )
        section_title.pack(pady=12)
        
        # Frame para los botones de módulos con mejor diseño
        buttons_frame = tk.Frame(modules_frame, bg=self.colors['light'])
        buttons_frame.pack(expand=True)
        
        # Configurar grid para mejor distribución
        for i in range(2):
            buttons_frame.grid_rowconfigure(i, weight=1)
            buttons_frame.grid_columnconfigure(i, weight=1)
        
        # Módulo 1: Gestión de Usuarios (mejorado)
        self.create_improved_module_button(
            buttons_frame,
            "👥",
            "GESTIÓN DE\nUSUARIOS",
            "Administración completa de usuarios\n• Crear y editar usuarios\n• Búsqueda avanzada\n• Control de estados",
            self.open_user_management,
            self.colors['primary'],
            0, 0
        )
        
        # Módulo 2: Registro de Pagos (mejorado)
        self.create_improved_module_button(
            buttons_frame,
            "💰",
            "REGISTRO DE\nPAGOS",
            "Control financiero profesional\n• Pagos mensuales\n• Conceptos adicionales\n• Recibos automáticos",
            self.open_payment_registration,
            self.colors['success'],
            0, 1
        )
        
        # Módulo 3: Configuración (mejorado)
        self.create_improved_module_button(
            buttons_frame,
            "⚙️",
            "CONFIGURACIÓN\nDEL SISTEMA",
            "Personalización avanzada\n• Gestión de tarifas\n• Conceptos de cobro\n• Respaldos automáticos",
            self.open_configuration,
            self.colors['warning'],
            1, 0
        )
        
        # Módulo 4: Importar CSV (útil)
        self.create_improved_module_button(
            buttons_frame,
            "📊",
            "IMPORTAR\nDATOS CSV",
            "Migración de datos externa\n• Importar usuarios masivamente\n• Validación automática\n• Reportes de importación",
            self.open_csv_importer,
            self.colors['danger'],
            1, 1
        )
    
    def create_improved_module_button(self, parent, icon, title, description, command, color, row, col):
        """Crea un botón mejorado para módulos"""
        # Contenedor principal con sombra simulada
        container = tk.Frame(parent, bg=self.colors['light'])
        container.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
        
        # Frame del botón con bordes elegantes
        button_frame = tk.Frame(container, bg=self.colors['white'], relief='solid', bd=2)
        button_frame.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        
        # Área del icono
        icon_frame = tk.Frame(button_frame, bg=color, height=80)
        icon_frame.pack(fill=tk.X)
        icon_frame.pack_propagate(False)
        
        icon_label = tk.Label(
            icon_frame,
            text=icon,
            font=('Segoe UI Emoji', 32),
            fg=self.colors['white'],
            bg=color
        )
        icon_label.pack(expand=True)
        
        # Área del contenido
        content_frame = tk.Frame(button_frame, bg=self.colors['white'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Título del módulo
        title_label = tk.Label(
            content_frame,
            text=title,
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['dark'],
            bg=self.colors['white'],
            justify=tk.CENTER
        )
        title_label.pack(pady=(0, 8))
        
        # Descripción detallada
        desc_label = tk.Label(
            content_frame,
            text=description,
            font=('Segoe UI', 9),
            fg='#7f8c8d',
            bg=self.colors['white'],
            wraplength=200,
            justify=tk.LEFT
        )
        desc_label.pack(pady=(0, 12))
        
        # Botón de acción
        action_button = tk.Button(
            content_frame,
            text="🚀 ACCEDER",
            command=command,
            font=('Segoe UI', 10, 'bold'),
            bg=color,
            fg=self.colors['white'],
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=8
        )
        action_button.pack(fill=tk.X)
        
        # Efectos hover mejorados
        def on_enter(e):
            button_frame.config(relief='raised', bd=3)
            action_button.config(bg=self.darken_color(color))
        
        def on_leave(e):
            button_frame.config(relief='solid', bd=2)
            action_button.config(bg=color)
        
        def on_click(e):
            command()
        
        # Bind eventos a todos los elementos para mejor UX
        for widget in [button_frame, icon_frame, icon_label, content_frame, title_label, desc_label]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", on_click)
    
    def create_elegant_footer(self, parent):
        """Crea el pie de la aplicación elegante"""
        # Footer con diseño profesional
        footer_frame = tk.Frame(parent, bg=self.colors['dark'], height=70)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)
        
        # Línea decorativa superior
        top_line = tk.Frame(footer_frame, bg=self.colors['primary'], height=3)
        top_line.pack(fill=tk.X)
        
        # Contenido del footer
        info_frame = tk.Frame(footer_frame, bg=self.colors['dark'])
        info_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=12)
        
        # Panel izquierdo - Información del sistema
        left_info = tk.Frame(info_frame, bg=self.colors['dark'])
        left_info.pack(side=tk.LEFT, fill=tk.Y)
        
        system_info = tk.Label(
            left_info,
            text="💧 Sistema Profesional de Gestión de Agua Potable",
            font=('Segoe UI', 10, 'bold'),
            fg=self.colors['white'],
            bg=self.colors['dark']
        )
        system_info.pack(anchor='w')
        
        dev_info = tk.Label(
            left_info,
            text="🏢 Desarrollado especialmente para comités de agua potable",
            font=('Segoe UI', 9),
            fg='#bdc3c7',
            bg=self.colors['dark']
        )
        dev_info.pack(anchor='w', pady=(2, 0))
        
        # Panel derecho - Estado del sistema
        right_info = tk.Frame(info_frame, bg=self.colors['dark'])
        right_info.pack(side=tk.RIGHT, fill=tk.Y)
        
        status_info = tk.Label(
            right_info,
            text="🟢 Sistema Operativo • Base de Datos Activa",
            font=('Segoe UI', 10, 'bold'),
            fg=self.colors['success'],
            bg=self.colors['dark']
        )
        status_info.pack(anchor='e')
        
        version_info = tk.Label(
            right_info,
            text="⚡ Versión 2.0 Professional Edition",
            font=('Segoe UI', 9),
            fg=self.colors['secondary'],
            bg=self.colors['dark']
        )
        version_info.pack(anchor='e', pady=(2, 0))
    
    def darken_color(self, color):
        """Oscurece un color hexadecimal para efectos hover"""
        color_map = {
            self.colors['primary']: "#1f5a8c",      # Azul más oscuro
            self.colors['secondary']: "#2980b9",    # Azul oscuro
            self.colors['success']: "#1e8449",      # Verde oscuro
            self.colors['warning']: "#d68910",      # Naranja oscuro
            self.colors['danger']: "#c0392b",       # Rojo oscuro
            "#3498db": "#2980b9",
            "#27ae60": "#229954",
            "#e74c3c": "#c0392b",
            "#9b59b6": "#8e44ad"
        }
        return color_map.get(color, color)
    
    # === FUNCIONES DE NAVEGACIÓN ===
    
    def open_user_management(self):
        """Abre el módulo de gestión de usuarios"""
        try:
            UserManagementWindow(self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir gestión de usuarios: {str(e)}")
    
    def open_payment_registration(self):
        """Abre el módulo de registro de pagos"""
        try:
            PaymentRegistrationWindow(self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir registro de pagos: {str(e)}")
    
    def open_configuration(self):
        """Abre el módulo de configuración"""
        try:
            ConfigurationWindow(self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir configuración: {str(e)}")
    
    def show_reports_placeholder(self):
        """Muestra un placeholder para el módulo de reportes"""
        messagebox.showinfo(
            "Módulo en Desarrollo",
            "El módulo de Reportes y Estadísticas estará disponible en una próxima actualización.\n\n" +
            "Características planificadas:\n" +
            "• Reportes de pagos por período\n" +
            "• Estadísticas de ingresos\n" +
            "• Listados de usuarios morosos\n" +
            "• Gráficos de tendencias\n" +
            "• Exportación a Excel/PDF"
        )
    
    def show_main_window(self):
        """Muestra la ventana principal"""
        self.root.deiconify()  # Mostrar la ventana si está minimizada
        self.root.lift()       # Traer al frente
        self.root.focus_force() # Dar foco
    
    def open_csv_importer(self):
        """Abre el importador de CSV"""
        try:
            from csv_importer import ImporterGUI
            importer = ImporterGUI()
            importer.run()
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir importador CSV: {str(e)}")
    
    def show_instructions(self):
        """Muestra las instrucciones del sistema"""
        instructions_window = tk.Toplevel(self.root)
        instructions_window.title("Instrucciones de Uso")
        instructions_window.geometry("600x500")
        instructions_window.resizable(True, True)
        
        # Frame con scroll
        canvas = tk.Canvas(instructions_window)
        scrollbar = ttk.Scrollbar(instructions_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Contenido de instrucciones
        instructions_text = """
INSTRUCCIONES DE USO - SISTEMA DE AGUA POTABLE

1. GESTIÓN DE USUARIOS
   • Nuevo Usuario: Crear usuarios con número, nombre, dirección, etc.
   • Buscar: Por número o nombre en tiempo real
   • Editar: Doble clic en usuario para modificar datos
   • Estado: Cambiar entre Activo/Cancelado
   • Historial: Ver todos los pagos de un usuario

2. REGISTRO DE PAGOS
   • Buscar usuario por número o nombre
   • Seleccionar año con las flechas
   • Clic en meses para marcar como pagados
   • Agregar conceptos adicionales (cooperaciones, multas)
   • Procesar pago y generar recibo automáticamente

3. CONFIGURACIÓN
   • Cuota Mensual: Modificar precio mensual del servicio
   • Conceptos: Agregar/editar conceptos adicionales de cobro
   • Información: Datos del comité para recibos
   • Seguridad: Cambiar PIN de acceso
   • Respaldos: Crear y restaurar copias de seguridad

4. ATAJOS DE TECLADO
   • Enter: Confirmar en diálogos
   • Escape: Cancelar operaciones
   • Ctrl+N: Nuevo usuario (en módulo usuarios)
   • F5: Actualizar listas

5. CONSEJOS
   • Crear respaldos regularmente
   • Cambiar el PIN por defecto (1234)
   • Verificar datos antes de procesar pagos
   • Los recibos se guardan en carpeta 'recibos/'
        """
        
        text_widget = tk.Text(
            scrollable_frame,
            wrap=tk.WORD,
            font=('Arial', 10),
            padx=10,
            pady=10
        )
        text_widget.insert("1.0", instructions_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botón cerrar
        close_btn = tk.Button(
            instructions_window,
            text="Cerrar",
            command=instructions_window.destroy,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 11)
        )
        close_btn.pack(pady=10)
    
    def show_about(self):
        """Muestra información sobre el sistema"""
        messagebox.showinfo(
            "Acerca del Sistema",
            "Sistema de Gestión de Agua Potable\n" +
            "Versión 1.0\n\n" +
            "Desarrollado en Python con Tkinter\n" +
            "Base de datos SQLite\n" +
            "Generación de PDF con ReportLab\n\n" +
            "Características:\n" +
            "• Gestión completa de usuarios\n" +
            "• Registro de pagos mensuales\n" +
            "• Conceptos adicionales de cobro\n" +
            "• Generación automática de recibos\n" +
            "• Sistema de respaldos\n" +
            "• Importación desde CSV\n\n" +
            "© 2024 - Desarrollado para comités de agua potable"
        )
    
    def on_closing(self):
        """Maneja el cierre de la aplicación"""
        if messagebox.askokcancel("Salir", "¿Está seguro de que desea salir del sistema?"):
            self.root.destroy()
    
    def run(self):
        """Ejecuta la aplicación principal"""
        self.root.mainloop()


def main():
    """Función principal de la aplicación"""
    try:
        # Autenticar usuario
        if not authenticate():
            print("Autenticación fallida. Cerrando aplicación.")
            return
        
        # Crear y ejecutar la aplicación principal
        app = MainApplication()
        app.run()
        
    except Exception as e:
        messagebox.showerror("Error Fatal", f"Error al iniciar la aplicación: {str(e)}")


if __name__ == "__main__":
    main()
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
        self.root.title("Sistema de Gestión de Agua Potable")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Configurar el icono de la ventana (si existe)
        self.set_window_icon()
        
        # Centrar la ventana
        self.center_window()
        
        # Variables
        self.logo_image = None
        self.example_image = None
        
        # Configurar la interfaz
        self.setup_ui()
        
        # Configurar eventos
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_menu(self):
        """Crea la barra de menú"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Sistema
        system_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Sistema", menu=system_menu)
        system_menu.add_command(label="🏠 Menú Principal", command=self.show_main_window)
        system_menu.add_separator()
        system_menu.add_command(label="📊 Importar CSV", command=self.open_csv_importer)
        system_menu.add_separator()
        system_menu.add_command(label="🚪 Salir", command=self.on_closing)
        
        # Menú Módulos
        modules_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Módulos", menu=modules_menu)
        modules_menu.add_command(label="👥 Gestión de Usuarios", command=self.open_user_management)
        modules_menu.add_command(label="💰 Registro de Pagos", command=self.open_payment_registration)
        modules_menu.add_command(label="⚙️ Configuración", command=self.open_configuration)
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="❓ Instrucciones", command=self.show_instructions)
        help_menu.add_command(label="ℹ️ Acerca de", command=self.show_about)
    
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
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Crear menú
        self.create_menu()
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#ecf0f1')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header con logo y título
        self.create_header(main_frame)
        
        # Área central con botones de módulos
        self.create_modules_area(main_frame)
        
        # Footer con información
        self.create_footer(main_frame)
    
    def create_header(self, parent):
        """Crea el encabezado de la aplicación"""
        header_frame = tk.Frame(parent, bg='#2c3e50', height=120)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Frame para el contenido del header
        content_frame = tk.Frame(header_frame, bg='#2c3e50')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Cargar y mostrar logo si existe
        if os.path.exists("logo.jpg"):
            try:
                logo_img = Image.open("logo.jpg")
                logo_img = logo_img.resize((80, 80), Image.Resampling.LANCZOS)
                self.logo_image = ImageTk.PhotoImage(logo_img)
                
                logo_label = tk.Label(
                    content_frame,
                    image=self.logo_image,
                    bg='#2c3e50'
                )
                logo_label.pack(side=tk.LEFT, padx=(0, 20))
            except Exception as e:
                print(f"Error al cargar logo: {e}")
        
        # Información del título
        title_frame = tk.Frame(content_frame, bg='#2c3e50')
        title_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Título principal
        title_label = tk.Label(
            title_frame,
            text="Sistema de Gestión de Agua Potable",
            font=('Arial', 20, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(anchor='w', pady=(5, 0))
        
        # Subtítulo
        subtitle_label = tk.Label(
            title_frame,
            text="Comité de Agua Potable - Gestión Integral",
            font=('Arial', 12),
            fg='#bdc3c7',
            bg='#2c3e50'
        )
        subtitle_label.pack(anchor='w')
        
        # Información de versión
        version_label = tk.Label(
            title_frame,
            text="Versión 1.0 - Desarrollado con Python",
            font=('Arial', 9),
            fg='#95a5a6',
            bg='#2c3e50'
        )
        version_label.pack(anchor='w', pady=(10, 0))
    
    def create_modules_area(self, parent):
        """Crea el área central con los módulos"""
        modules_frame = tk.Frame(parent, bg='#ecf0f1')
        modules_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título de la sección
        section_title = tk.Label(
            modules_frame,
            text="Módulos del Sistema",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        )
        section_title.pack(pady=(0, 20))
        
        # Frame para los botones de módulos (2x2 grid)
        buttons_frame = tk.Frame(modules_frame, bg='#ecf0f1')
        buttons_frame.pack(expand=True)
        
        # Módulo 1: Gestión de Usuarios
        self.create_module_button(
            buttons_frame,
            "👥\nGestión de\nUsuarios",
            "Crear, buscar y administrar\ninformación de usuarios",
            self.open_user_management,
            "#3498db",
            0, 0
        )
        
        # Módulo 2: Registro de Pagos
        self.create_module_button(
            buttons_frame,
            "💰\nRegistro de\nPagos",
            "Procesar pagos mensuales\ny conceptos adicionales",
            self.open_payment_registration,
            "#27ae60",
            0, 1
        )
        
        # Módulo 3: Configuración
        self.create_module_button(
            buttons_frame,
            "⚙️\nConfiguración\ndel Sistema",
            "Gestionar tarifas, conceptos\ny configuración general",
            self.open_configuration,
            "#e74c3c",
            1, 0
        )
        
        # Módulo 4: Reportes (placeholder)
        self.create_module_button(
            buttons_frame,
            "📊\nReportes y\nEstadísticas",
            "Generas reportes de pagos\ny estadísticas del sistema",
            self.show_reports_placeholder,
            "#9b59b6",
            1, 1
        )
    
    def create_module_button(self, parent, title, description, command, color, row, col):
        """Crea un botón para un módulo"""
        # Frame contenedor para el botón
        button_frame = tk.Frame(parent, bg='#ecf0f1')
        button_frame.grid(row=row, column=col, padx=20, pady=15, sticky='nsew')
        
        # Configurar grid weights
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        # Botón principal
        main_button = tk.Button(
            button_frame,
            text=title,
            command=command,
            font=('Arial', 14, 'bold'),
            bg=color,
            fg='white',
            width=15,
            height=6,
            relief=tk.RAISED,
            bd=3,
            cursor='hand2'
        )
        main_button.pack(fill=tk.BOTH, expand=True)
        
        # Descripción debajo del botón
        desc_label = tk.Label(
            button_frame,
            text=description,
            font=('Arial', 9),
            fg='#7f8c8d',
            bg='#ecf0f1',
            wraplength=180,
            justify=tk.CENTER
        )
        desc_label.pack(pady=(5, 0))
        
        # Efectos hover
        def on_enter(e):
            main_button.config(bg=self.darken_color(color))
        
        def on_leave(e):
            main_button.config(bg=color)
        
        main_button.bind("<Enter>", on_enter)
        main_button.bind("<Leave>", on_leave)
    
    def create_footer(self, parent):
        """Crea el pie de la aplicación"""
        footer_frame = tk.Frame(parent, bg='#34495e', height=60)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)
        
        # Información del pie
        info_frame = tk.Frame(footer_frame, bg='#34495e')
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Información del sistema
        system_info = tk.Label(
            info_frame,
            text="Sistema desarrollado para la gestión eficiente de comités de agua potable",
            font=('Arial', 10),
            fg='#bdc3c7',
            bg='#34495e'
        )
        system_info.pack(side=tk.LEFT)
        
        # Información de estado
        status_info = tk.Label(
            info_frame,
            text="Sistema Activo • Base de Datos Conectada",
            font=('Arial', 9),
            fg='#2ecc71',
            bg='#34495e'
        )
        status_info.pack(side=tk.RIGHT)
    
    def darken_color(self, color):
        """Oscurece un color hexadecimal para efectos hover"""
        color_map = {
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
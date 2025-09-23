#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de gestión de usuarios para el sistema de agua potable
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database import get_db_manager
from typing import Dict, List, Optional

class UserManagementWindow:
    def __init__(self, parent=None):
        # Crear ventana principal o usar la proporcionada
        if parent:
            self.root = tk.Toplevel(parent)
        else:
            self.root = tk.Tk()
        
        self.root.title("Gestión de Usuarios")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        self.root.state('zoomed') if hasattr(self.root, 'state') else None  # Maximizar en Windows
        
        # Variables
        self.current_user = None
        self.users_data = []
        
        # Configurar la interfaz
        self.setup_ui()
        
        # Cargar datos iniciales
        self.refresh_users_list()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Frame principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="Gestión de Usuarios",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 10))
        
        # Frame superior para búsqueda y controles
        top_frame = tk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.create_search_controls(top_frame)
        
        # Frame central dividido en dos columnas
        center_frame = tk.Frame(main_frame)
        center_frame.pack(fill=tk.BOTH, expand=True)
        
        # Columna izquierda: Lista de usuarios
        left_frame = tk.LabelFrame(center_frame, text="Lista de Usuarios", font=('Arial', 12, 'bold'))
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.create_users_list(left_frame)
        
        # Columna derecha: Detalles y edición
        right_frame = tk.LabelFrame(center_frame, text="Detalles del Usuario", font=('Arial', 12, 'bold'))
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.create_user_details(right_frame)
        
        # Frame inferior para botones principales
        bottom_frame = tk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.create_main_buttons(bottom_frame)
    
    def create_search_controls(self, parent):
        """Crea los controles de búsqueda"""
        # Frame para la búsqueda
        search_frame = tk.Frame(parent)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Búsqueda por número
        tk.Label(
            search_frame, 
            text="Buscar por número:", 
            font=('Arial', 11, 'bold'),
            fg='#2c3e50'
        ).pack(side=tk.LEFT)
        
        self.search_number_var = tk.StringVar()
        search_number_entry = tk.Entry(
            search_frame,
            textvariable=self.search_number_var,
            width=10,
            font=('Arial', 12),
            bg='white',
            fg='#2c3e50',
            relief='solid',
            bd=1,
            insertbackground='#3498db'
        )
        search_number_entry.pack(side=tk.LEFT, padx=(5, 15))
        search_number_entry.bind('<KeyRelease>', self.on_search_change)
        
        # Búsqueda por nombre
        tk.Label(
            search_frame, 
            text="Buscar por nombre:", 
            font=('Arial', 11, 'bold'),
            fg='#2c3e50'
        ).pack(side=tk.LEFT)
        
        self.search_name_var = tk.StringVar()
        search_name_entry = tk.Entry(
            search_frame,
            textvariable=self.search_name_var,
            width=20,
            font=('Arial', 12),
            bg='white',
            fg='#2c3e50',
            relief='solid',
            bd=1,
            insertbackground='#3498db'
        )
        search_name_entry.pack(side=tk.LEFT, padx=(5, 15))
        search_name_entry.bind('<KeyRelease>', self.on_search_change)
        
        # Filtro por estado
        tk.Label(
            search_frame, 
            text="Estado:", 
            font=('Arial', 11, 'bold'),
            fg='#2c3e50'
        ).pack(side=tk.LEFT)
        
        self.status_filter_var = tk.StringVar(value="Todos")
        status_combo = ttk.Combobox(
            search_frame,
            textvariable=self.status_filter_var,
            values=["Todos", "Activo", "Cancelado"],
            state="readonly",
            width=10,
            font=('Arial', 12),
            height=6
        )
        status_combo.pack(side=tk.LEFT, padx=(5, 10))
        status_combo.bind('<<ComboboxSelected>>', self.on_search_change)
        
        # Botón limpiar búsqueda
        clear_btn = tk.Button(
            search_frame,
            text="Limpiar",
            command=self.clear_search,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 9)
        )
        clear_btn.pack(side=tk.LEFT, padx=(5, 0))
    
    def create_users_list(self, parent):
        """Crea la lista de usuarios con Treeview"""
        # Frame para la lista
        list_frame = tk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Crear Treeview
        columns = ('numero', 'nombre', 'estado')
        self.users_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        self.users_tree.heading('numero', text='Número')
        self.users_tree.heading('nombre', text='Nombre')
        self.users_tree.heading('estado', text='Estado')
        
        self.users_tree.column('numero', width=80, anchor='center')
        self.users_tree.column('nombre', width=200)
        self.users_tree.column('estado', width=80, anchor='center')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.users_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.users_tree.xview)
        
        self.users_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Posicionar elementos
        self.users_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Eventos
        self.users_tree.bind('<<TreeviewSelect>>', self.on_user_select)
        self.users_tree.bind('<Double-1>', self.on_user_double_click)
    
    def create_user_details(self, parent):
        """Crea el panel de detalles del usuario"""
        # Frame principal para detalles
        details_frame = tk.Frame(parent)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Variables para los campos
        self.user_id_var = tk.StringVar()
        self.user_number_var = tk.StringVar()
        self.user_name_var = tk.StringVar()
        self.user_address_var = tk.StringVar()
        self.user_phone_var = tk.StringVar()
        self.user_email_var = tk.StringVar()
        self.user_status_var = tk.StringVar()
        
        # Campos del formulario
        fields = [
            ("ID:", self.user_id_var, True),  # True = readonly
            ("Número:", self.user_number_var, False),
            ("Nombre:", self.user_name_var, False),
            ("Dirección:", self.user_address_var, False),
            ("Teléfono:", self.user_phone_var, False),
            ("Email:", self.user_email_var, False)
        ]
        
        self.entry_widgets = {}
        
        for i, (label_text, var, readonly) in enumerate(fields):
            # Frame para cada campo
            field_frame = tk.Frame(details_frame)
            field_frame.pack(fill=tk.X, pady=8)
            
            # Label con mejor estilo
            label = tk.Label(
                field_frame, 
                text=label_text, 
                font=('Arial', 11, 'bold'), 
                width=12, 
                anchor='w',
                fg='#2c3e50'
            )
            label.pack(side=tk.LEFT)
            
            # Entry con mejor legibilidad
            if readonly:
                entry = tk.Entry(
                    field_frame,
                    textvariable=var,
                    font=('Arial', 12, 'bold'),
                    state='readonly',
                    bg='#ecf0f1',
                    fg='#2c3e50',
                    relief='solid',
                    bd=1,
                    justify='center'
                )
            else:
                entry = tk.Entry(
                    field_frame,
                    textvariable=var,
                    font=('Arial', 12),
                    bg='white',
                    fg='#2c3e50',
                    relief='solid',
                    bd=1,
                    insertbackground='#3498db'
                )
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
            
            self.entry_widgets[label_text.replace(':', '')] = entry
        
        # Campo estado (ComboBox)
        status_frame = tk.Frame(details_frame)
        status_frame.pack(fill=tk.X, pady=8)
        
        status_label = tk.Label(
            status_frame, 
            text="Estado:", 
            font=('Arial', 11, 'bold'), 
            width=12, 
            anchor='w',
            fg='#2c3e50'
        )
        status_label.pack(side=tk.LEFT)
        
        self.status_combo = ttk.Combobox(
            status_frame,
            textvariable=self.user_status_var,
            values=["Activo", "Cancelado"],
            state="readonly",
            font=('Arial', 12),
            height=6
        )
        self.status_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        # Botones de acción
        buttons_frame = tk.Frame(details_frame)
        buttons_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.save_btn = tk.Button(
            buttons_frame,
            text="Guardar Cambios",
            command=self.save_user_changes,
            bg='#27ae60',
            fg='white',
            font=('Arial', 10, 'bold'),
            state='disabled'
        )
        self.save_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.cancel_btn = tk.Button(
            buttons_frame,
            text="Cancelar",
            command=self.cancel_changes,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 10),
            state='disabled'
        )
        self.cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def create_main_buttons(self, parent):
        """Crea los botones principales"""
        # Botón nuevo usuario
        new_user_btn = tk.Button(
            parent,
            text="Nuevo Usuario",
            command=self.show_new_user_dialog,
            bg='#3498db',
            fg='white',
            font=('Arial', 12, 'bold'),
            height=2
        )
        new_user_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón ver historial de pagos
        self.history_btn = tk.Button(
            parent,
            text="Ver Historial de Pagos",
            command=self.show_payment_history,
            bg='#9b59b6',
            fg='white',
            font=('Arial', 12, 'bold'),
            height=2,
            state='disabled'
        )
        self.history_btn.pack(side=tk.LEFT, padx=5)
        
        # Botón cerrar
        close_btn = tk.Button(
            parent,
            text="Cerrar",
            command=self.root.destroy,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 12),
            height=2
        )
        close_btn.pack(side=tk.RIGHT)
    
    def refresh_users_list(self):
        """Actualiza la lista de usuarios"""
        try:
            db = get_db_manager()
            
            # Obtener filtros
            search_number = self.search_number_var.get().strip() if hasattr(self, 'search_number_var') else ""
            search_name = self.search_name_var.get().strip() if hasattr(self, 'search_name_var') else ""
            status_filter = self.status_filter_var.get() if hasattr(self, 'status_filter_var') else "Todos"
            
            # Obtener usuarios
            if search_number:
                try:
                    numero = int(search_number)
                    user = db.buscar_usuario_por_numero(numero)
                    self.users_data = [user] if user else []
                except ValueError:
                    self.users_data = []
            elif search_name:
                self.users_data = db.buscar_usuarios_por_nombre(search_name)
            else:
                self.users_data = db.obtener_todos_usuarios()
            
            # Aplicar filtro de estado
            if status_filter != "Todos":
                self.users_data = [user for user in self.users_data if user['estado'] == status_filter]
            
            # Limpiar el Treeview
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)
            
            # Llenar el Treeview
            for user in self.users_data:
                self.users_tree.insert('', 'end', values=(
                    user['numero'],
                    user['nombre'],
                    user['estado']
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar usuarios: {str(e)}")
    
    def on_search_change(self, event=None):
        """Maneja los cambios en los campos de búsqueda"""
        self.refresh_users_list()
    
    def clear_search(self):
        """Limpia los campos de búsqueda"""
        self.search_number_var.set("")
        self.search_name_var.set("")
        self.status_filter_var.set("Todos")
        self.refresh_users_list()
    
    def on_user_select(self, event):
        """Maneja la selección de un usuario en la lista"""
        selection = self.users_tree.selection()
        if not selection:
            self.clear_user_details()
            return
        
        # Obtener el usuario seleccionado
        item = self.users_tree.item(selection[0])
        numero = item['values'][0]
        
        # Buscar el usuario completo en los datos
        user = next((u for u in self.users_data if u['numero'] == numero), None)
        if user:
            self.load_user_details(user)
    
    def on_user_double_click(self, event):
        """Maneja el doble clic en un usuario"""
        self.enable_editing()
    
    def load_user_details(self, user: Dict):
        """Carga los detalles de un usuario en el panel derecho"""
        self.current_user = user
        
        self.user_id_var.set(str(user['id']))
        self.user_number_var.set(str(user['numero']))
        self.user_name_var.set(user['nombre'] or '')
        self.user_address_var.set(user['direccion'] or '')
        self.user_phone_var.set(user['telefono'] or '')
        self.user_email_var.set(user['email'] or '')
        self.user_status_var.set(user['estado'])
        
        # Habilitar botón de historial
        self.history_btn.config(state='normal')
        
        # Deshabilitar edición inicialmente
        self.disable_editing()
    
    def clear_user_details(self):
        """Limpia los detalles del usuario"""
        self.current_user = None
        
        for var in [self.user_id_var, self.user_number_var, self.user_name_var,
                   self.user_address_var, self.user_phone_var, self.user_email_var]:
            var.set("")
        
        self.user_status_var.set("")
        
        # Deshabilitar botones
        self.history_btn.config(state='disabled')
        self.disable_editing()
    
    def enable_editing(self):
        """Habilita la edición de los campos del usuario"""
        if not self.current_user:
            return
        
        # Habilitar campos editables
        for field_name, entry in self.entry_widgets.items():
            if field_name != "ID":  # ID no es editable
                entry.config(state='normal')
        
        self.status_combo.config(state='readonly')
        
        # Habilitar botones de acción
        self.save_btn.config(state='normal')
        self.cancel_btn.config(state='normal')
    
    def disable_editing(self):
        """Deshabilita la edición de los campos del usuario"""
        # Deshabilitar campos
        for entry in self.entry_widgets.values():
            entry.config(state='readonly')
        
        self.status_combo.config(state='disabled')
        
        # Deshabilitar botones de acción
        self.save_btn.config(state='disabled')
        self.cancel_btn.config(state='disabled')
    
    def save_user_changes(self):
        """Guarda los cambios realizados al usuario"""
        if not self.current_user:
            return
        
        try:
            # Validar datos
            numero = self.user_number_var.get().strip()
            nombre = self.user_name_var.get().strip()
            
            if not numero or not nombre:
                messagebox.showwarning("Advertencia", "El número y nombre son obligatorios")
                return
            
            try:
                numero = int(numero)
            except ValueError:
                messagebox.showwarning("Advertencia", "El número debe ser un valor numérico")
                return
            
            # Preparar datos para actualizar
            datos_actualizar = {
                'numero': numero,
                'nombre': nombre,
                'direccion': self.user_address_var.get().strip(),
                'telefono': self.user_phone_var.get().strip(),
                'email': self.user_email_var.get().strip(),
                'estado': self.user_status_var.get()
            }
            
            # Actualizar en la base de datos
            db = get_db_manager()
            if db.actualizar_usuario(self.current_user['id'], **datos_actualizar):
                messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
                self.disable_editing()
                self.refresh_users_list()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el usuario")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar cambios: {str(e)}")
    
    def cancel_changes(self):
        """Cancela los cambios y restaura los valores originales"""
        if self.current_user:
            self.load_user_details(self.current_user)
        self.disable_editing()
    
    def show_new_user_dialog(self):
        """Muestra el diálogo para crear un nuevo usuario"""
        dialog = NewUserDialog(self.root)
        if dialog.result:
            self.refresh_users_list()
    
    def show_payment_history(self):
        """Muestra el historial de pagos del usuario seleccionado"""
        if not self.current_user:
            return
        
        try:
            db = get_db_manager()
            pagos = db.obtener_historial_pagos_usuario(self.current_user['id'])
            
            # Crear ventana de historial
            PaymentHistoryWindow(self.root, self.current_user, pagos)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener historial: {str(e)}")


class NewUserDialog:
    def __init__(self, parent):
        self.result = None
        
        # Crear ventana modal
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Nuevo Usuario")
        self.dialog.geometry("400x350")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar la ventana
        self.center_window()
        
        # Variables
        self.number_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        
        # Obtener y asignar el siguiente número automáticamente
        self.auto_assign_number()
        
        # Configurar la interfaz
        self.setup_ui()
        
        # Enfocar el campo de nombre (ya que el número es automático)
        self.name_entry.focus()
    
    def auto_assign_number(self):
        """Asigna automáticamente el siguiente número disponible"""
        try:
            db = get_db_manager()
            next_number = db.get_next_user_number()
            self.number_var.set(str(next_number))
        except Exception as e:
            # En caso de error, usar 1 como valor por defecto
            self.number_var.set("1")
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Configura la interfaz del diálogo"""
        # Frame principal
        main_frame = tk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="Crear Nuevo Usuario",
            font=('Arial', 14, 'bold'),
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 20))
        
        # Campos del formulario
        fields = [
            ("Número:", self.number_var, True, True),   # True = obligatorio, True = readonly
            ("Nombre:", self.name_var, True, False),
            ("Dirección:", self.address_var, False, False),
            ("Teléfono:", self.phone_var, False, False),
            ("Email:", self.email_var, False, False)
        ]
        
        for label_text, var, required, readonly in fields:
            # Frame para cada campo
            field_frame = tk.Frame(main_frame)
            field_frame.pack(fill=tk.X, pady=8)
            
            # Label con asterisco si es obligatorio
            label_display = f"{label_text} *" if required else label_text
            if label_text == "Número:":
                label_display += " (Automático)"
            
            label = tk.Label(
                field_frame, 
                text=label_display, 
                font=('Arial', 11, 'bold'), 
                width=15, 
                anchor='w',
                fg='#2c3e50'
            )
            label.pack(side=tk.LEFT)
            
            # Entry con mejores estilos para legibilidad
            if readonly:
                entry = tk.Entry(
                    field_frame, 
                    textvariable=var, 
                    font=('Arial', 12, 'bold'),
                    state='readonly',
                    bg='#ecf0f1',
                    fg='#2c3e50',
                    relief='solid',
                    bd=1,
                    justify='center'
                )
            else:
                entry = tk.Entry(
                    field_frame, 
                    textvariable=var, 
                    font=('Arial', 12),
                    bg='white',
                    fg='#2c3e50',
                    relief='solid',
                    bd=1,
                    insertbackground='#3498db'
                )
            
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
            
            # Guardar referencias
            if label_text == "Número:":
                self.number_entry = entry
            elif label_text == "Nombre:":
                self.name_entry = entry
        
        # Nota sobre campos obligatorios
        note_label = tk.Label(
            main_frame,
            text="* Campos obligatorios",
            font=('Arial', 8),
            fg='#7f8c8d'
        )
        note_label.pack(pady=(10, 20))
        
        # Botones
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X)
        
        create_btn = tk.Button(
            buttons_frame,
            text="Crear Usuario",
            command=self.create_user,
            bg='#27ae60',
            fg='white',
            font=('Arial', 11, 'bold'),
            width=15
        )
        create_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = tk.Button(
            buttons_frame,
            text="Cancelar",
            command=self.dialog.destroy,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 11),
            width=15
        )
        cancel_btn.pack(side=tk.LEFT)
        
        # Bind Enter key
        self.dialog.bind('<Return>', lambda e: self.create_user())
    
    def create_user(self):
        """Crea el nuevo usuario"""
        try:
            # Validar campos obligatorios
            numero = self.number_var.get().strip()
            nombre = self.name_var.get().strip()
            
            if not nombre:
                messagebox.showwarning("Advertencia", "Por favor ingrese el nombre del usuario")
                self.name_entry.focus()
                return
            
            # El número ya está asignado automáticamente, pero validamos por seguridad
            if not numero:
                messagebox.showerror("Error", "Error interno: No se pudo asignar número automáticamente")
                return
            
            # Validar que el número sea numérico
            try:
                numero = int(numero)
            except ValueError:
                messagebox.showerror("Error", "Error interno: Número inválido")
                return
            
            # Crear el usuario
            db = get_db_manager()
            if db.crear_usuario(
                numero=numero,
                nombre=nombre,
                direccion=self.address_var.get().strip(),
                telefono=self.phone_var.get().strip(),
                email=self.email_var.get().strip()
            ):
                messagebox.showinfo("Éxito", "Usuario creado correctamente")
                self.result = True
                self.dialog.destroy()
            else:
                messagebox.showerror("Error", "Ya existe un usuario con ese número")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear usuario: {str(e)}")


class PaymentHistoryWindow:
    def __init__(self, parent, user: Dict, payments: List[Dict]):
        self.root = tk.Toplevel(parent)
        self.root.title(f"Historial de Pagos - {user['nombre']}")
        self.root.geometry("800x600")
        self.root.transient(parent)
        
        self.user = user
        self.payments = payments
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz del historial"""
        # Frame principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text=f"Historial de Pagos - Usuario #{self.user['numero']}: {self.user['nombre']}",
            font=('Arial', 14, 'bold'),
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 10))
        
        # Lista de pagos
        columns = ('fecha', 'total', 'detalles')
        tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=20)
        
        tree.heading('fecha', text='Fecha')
        tree.heading('total', text='Total')
        tree.heading('detalles', text='Detalles')
        
        tree.column('fecha', width=150)
        tree.column('total', width=100, anchor='center')
        tree.column('detalles', width=400)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Llenar con datos
        for pago in self.payments:
            fecha = pago['fecha_pago'][:16] if pago['fecha_pago'] else 'N/A'  # Solo fecha y hora
            total = f"${pago['total']:.2f}"
            
            # Crear resumen de detalles
            detalles = []
            for detalle in pago['detalles']:
                if detalle['mes']:
                    detalles.append(f"Mes {detalle['mes']}/{detalle['anio']}")
                else:
                    detalles.append(detalle['concepto'])
            
            detalles_str = ", ".join(detalles)
            
            tree.insert('', 'end', values=(fecha, total, detalles_str))
        
        # Botón cerrar
        close_btn = tk.Button(
            main_frame,
            text="Cerrar",
            command=self.root.destroy,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 11)
        )
        close_btn.pack(pady=(10, 0))
    
    # === FUNCIONES DE NAVEGACIÓN ===
    
    def open_payment_registration(self):
        """Abre el módulo de registro de pagos"""
        try:
            from payment_registration import PaymentRegistrationWindow
            PaymentRegistrationWindow(self.parent)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir registro de pagos: {str(e)}")
    
    def open_configuration(self):
        """Abre el módulo de configuración"""
        try:
            from configuration import ConfigurationWindow
            ConfigurationWindow(self.parent)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir configuración: {str(e)}")
    
    def open_main_window(self):
        """Abre la ventana principal"""
        try:
            # Cerrar esta ventana y abrir la principal
            self.window.destroy()
            from main import MainApplication
            app = MainApplication()
            app.run()
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir menú principal: {str(e)}")


def main():
    """Función principal para probar el módulo"""
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    
    app = UserManagementWindow()
    root.mainloop()


if __name__ == "__main__":
    main()
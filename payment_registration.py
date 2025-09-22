#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de registro de pagos para el sistema de agua potable
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database import get_db_manager
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class PaymentRegistrationWindow:
    def __init__(self, parent=None):
        # Crear ventana principal o usar la proporcionada
        if parent:
            self.root = tk.Toplevel(parent)
        else:
            self.root = tk.Tk()
        
        self.root.title("Registro de Pagos")
        self.root.geometry("1100x800")
        self.root.resizable(True, True)
        self.root.state('zoomed') if hasattr(self.root, 'state') else None  # Maximizar en Windows
        
        # Variables
        self.current_user = None
        self.current_year = datetime.now().year
        self.paid_months = []
        self.selected_months = []
        self.additional_concepts = []
        self.month_buttons = {}
        
        # Configurar la interfaz
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Frame principal con scroll
        main_canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        self.scrollable_frame = tk.Frame(main_canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame principal
        main_frame = tk.Frame(self.scrollable_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Empaquetar canvas y scrollbar
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Habilitar scroll con rueda del mouse
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="Registro de Pagos",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 10))
        
        # Frame superior para búsqueda de usuario
        self.create_user_search_section(main_frame)
        
        # Frame central para información del usuario
        self.create_user_info_section(main_frame)
        
        # Frame para selección de año
        self.create_year_selection(main_frame)
        
        # Frame para calendario de meses
        self.create_month_calendar(main_frame)
        
        # Frame para conceptos adicionales
        self.create_additional_concepts_section(main_frame)
        
        # Frame para totales y pago
        self.create_payment_section(main_frame)
    
    def create_user_search_section(self, parent):
        """Crea la sección de búsqueda de usuario"""
        search_frame = tk.LabelFrame(parent, text="Buscar Usuario", font=('Arial', 12, 'bold'))
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Frame interno
        inner_frame = tk.Frame(search_frame)
        inner_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Búsqueda por número
        tk.Label(inner_frame, text="Número:", font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.search_number_var = tk.StringVar()
        self.search_number_entry = tk.Entry(
            inner_frame,
            textvariable=self.search_number_var,
            width=10,
            font=('Arial', 10)
        )
        self.search_number_entry.pack(side=tk.LEFT, padx=(5, 10))
        self.search_number_entry.bind('<Return>', self.search_user_by_number)
        
        # Botón buscar por número
        search_num_btn = tk.Button(
            inner_frame,
            text="Buscar",
            command=self.search_user_by_number,
            bg='#3498db',
            fg='white',
            font=('Arial', 9)
        )
        search_num_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        # Separador
        tk.Label(inner_frame, text="|", font=('Arial', 10)).pack(side=tk.LEFT, padx=10)
        
        # Búsqueda por nombre
        tk.Label(inner_frame, text="Nombre:", font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.search_name_var = tk.StringVar()
        self.search_name_entry = tk.Entry(
            inner_frame,
            textvariable=self.search_name_var,
            width=20,
            font=('Arial', 10)
        )
        self.search_name_entry.pack(side=tk.LEFT, padx=(5, 10))
        self.search_name_entry.bind('<KeyRelease>', self.on_name_search_change)
        
        # Lista de sugerencias para nombres
        self.name_suggestions = tk.Listbox(
            search_frame,
            height=3,
            font=('Arial', 9)
        )
        self.name_suggestions.bind('<Double-Button-1>', self.select_user_from_suggestions)
        # Inicialmente oculto
        self.name_suggestions.pack_forget()
    
    def create_user_info_section(self, parent):
        """Crea la sección de información del usuario"""
        self.user_info_frame = tk.LabelFrame(parent, text="Usuario Seleccionado", font=('Arial', 12, 'bold'))
        self.user_info_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Información del usuario (inicialmente vacía)
        self.user_info_label = tk.Label(
            self.user_info_frame,
            text="No hay usuario seleccionado",
            font=('Arial', 11),
            fg='#7f8c8d'
        )
        self.user_info_label.pack(pady=10)
    
    def create_year_selection(self, parent):
        """Crea la sección de selección de año"""
        year_frame = tk.Frame(parent)
        year_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(year_frame, text="Año:", font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        
        # Botón año anterior
        prev_year_btn = tk.Button(
            year_frame,
            text="◀",
            command=self.prev_year,
            font=('Arial', 12),
            width=3
        )
        prev_year_btn.pack(side=tk.LEFT, padx=(10, 5))
        
        # Label del año actual
        self.year_label = tk.Label(
            year_frame,
            text=str(self.current_year),
            font=('Arial', 14, 'bold'),
            fg='#2c3e50',
            width=6
        )
        self.year_label.pack(side=tk.LEFT, padx=5)
        
        # Botón año siguiente
        next_year_btn = tk.Button(
            year_frame,
            text="▶",
            command=self.next_year,
            font=('Arial', 12),
            width=3
        )
        next_year_btn.pack(side=tk.LEFT, padx=(5, 0))
    
    def create_month_calendar(self, parent):
        """Crea el calendario de 12 meses"""
        calendar_frame = tk.LabelFrame(parent, text="Seleccionar Meses a Pagar", font=('Arial', 12, 'bold'))
        calendar_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Grid para los meses (3 filas x 4 columnas)
        months_grid = tk.Frame(calendar_frame)
        months_grid.pack(pady=10)
        
        months_names = [
            "Enero", "Febrero", "Marzo", "Abril",
            "Mayo", "Junio", "Julio", "Agosto",
            "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        
        for i, month_name in enumerate(months_names):
            row = i // 4
            col = i % 4
            month_num = i + 1
            
            # Crear botón para cada mes
            btn = tk.Button(
                months_grid,
                text=month_name,
                font=('Arial', 10),
                width=12,
                height=3,
                command=lambda m=month_num: self.toggle_month_selection(m),
                relief=tk.RAISED,
                bd=2
            )
            btn.grid(row=row, column=col, padx=5, pady=5)
            
            self.month_buttons[month_num] = btn
        
        # Botones de selección masiva
        mass_select_frame = tk.Frame(calendar_frame)
        mass_select_frame.pack(pady=10)
        
        select_all_btn = tk.Button(
            mass_select_frame,
            text="Seleccionar Todos",
            command=self.select_all_months,
            bg='#27ae60',
            fg='white',
            font=('Arial', 10)
        )
        select_all_btn.pack(side=tk.LEFT, padx=5)
        
        clear_all_btn = tk.Button(
            mass_select_frame,
            text="Limpiar Selección",
            command=self.clear_month_selection,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 10)
        )
        clear_all_btn.pack(side=tk.LEFT, padx=5)
        
        # Información sobre cuota mensual
        self.monthly_fee_label = tk.Label(
            calendar_frame,
            text="Cuota mensual: $0.00",
            font=('Arial', 10),
            fg='#7f8c8d'
        )
        self.monthly_fee_label.pack(pady=(5, 0))
        
        # Actualizar la cuota mensual
        self.update_monthly_fee_display()
    
    def create_additional_concepts_section(self, parent):
        """Crea la sección de conceptos adicionales"""
        concepts_frame = tk.LabelFrame(parent, text="Conceptos Adicionales", font=('Arial', 12, 'bold'))
        concepts_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Frame para agregar conceptos
        add_concept_frame = tk.Frame(concepts_frame)
        add_concept_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(add_concept_frame, text="Concepto:", font=('Arial', 10)).pack(side=tk.LEFT)
        
        # ComboBox para seleccionar concepto
        self.concept_var = tk.StringVar()
        self.concept_combo = ttk.Combobox(
            add_concept_frame,
            textvariable=self.concept_var,
            state="readonly",
            width=20,
            font=('Arial', 10)
        )
        self.concept_combo.pack(side=tk.LEFT, padx=(5, 10))
        self.concept_combo.bind('<<ComboboxSelected>>', self.on_concept_selected)
        
        tk.Label(add_concept_frame, text="Precio:", font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.concept_price_var = tk.StringVar()
        self.concept_price_entry = tk.Entry(
            add_concept_frame,
            textvariable=self.concept_price_var,
            width=10,
            font=('Arial', 10)
        )
        self.concept_price_entry.pack(side=tk.LEFT, padx=(5, 10))
        
        add_concept_btn = tk.Button(
            add_concept_frame,
            text="Agregar",
            command=self.add_additional_concept,
            bg='#f39c12',
            fg='white',
            font=('Arial', 10)
        )
        add_concept_btn.pack(side=tk.LEFT, padx=5)
        
        # Lista de conceptos agregados
        self.concepts_listbox = tk.Listbox(
            concepts_frame,
            height=4,
            font=('Arial', 9)
        )
        self.concepts_listbox.pack(fill=tk.X, padx=10, pady=5)
        
        # Botón para eliminar concepto seleccionado
        remove_concept_btn = tk.Button(
            concepts_frame,
            text="Eliminar Seleccionado",
            command=self.remove_selected_concept,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 9)
        )
        remove_concept_btn.pack(pady=5)
        
        # Cargar conceptos disponibles
        self.load_available_concepts()
    
    def create_payment_section(self, parent):
        """Crea la sección de pago y totales"""
        payment_frame = tk.LabelFrame(parent, text="Resumen de Pago", font=('Arial', 12, 'bold'))
        payment_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Frame para totales
        totals_frame = tk.Frame(payment_frame)
        totals_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Total mensualidades
        self.monthly_total_label = tk.Label(
            totals_frame,
            text="Mensualidades: $0.00",
            font=('Arial', 11),
            anchor='w'
        )
        self.monthly_total_label.pack(fill=tk.X)
        
        # Total conceptos adicionales
        self.concepts_total_label = tk.Label(
            totals_frame,
            text="Conceptos adicionales: $0.00",
            font=('Arial', 11),
            anchor='w'
        )
        self.concepts_total_label.pack(fill=tk.X)
        
        # Separador
        tk.Frame(totals_frame, height=2, bg='#bdc3c7').pack(fill=tk.X, pady=5)
        
        # Total general
        self.total_label = tk.Label(
            totals_frame,
            text="TOTAL A PAGAR: $0.00",
            font=('Arial', 14, 'bold'),
            fg='#27ae60',
            anchor='w'
        )
        self.total_label.pack(fill=tk.X)
        
        # Frame para observaciones
        obs_frame = tk.Frame(payment_frame)
        obs_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        tk.Label(obs_frame, text="Observaciones:", font=('Arial', 10)).pack(anchor='w')
        
        self.observations_text = tk.Text(
            obs_frame,
            height=3,
            font=('Arial', 10),
            wrap=tk.WORD
        )
        self.observations_text.pack(fill=tk.X, pady=(5, 0))
        
        # Botones de acción
        buttons_frame = tk.Frame(payment_frame)
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.process_payment_btn = tk.Button(
            buttons_frame,
            text="Procesar Pago",
            command=self.process_payment,
            bg='#27ae60',
            fg='white',
            font=('Arial', 12, 'bold'),
            height=2,
            state='disabled'
        )
        self.process_payment_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = tk.Button(
            buttons_frame,
            text="Limpiar Todo",
            command=self.clear_all,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 12),
            height=2
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Botones de navegación
        users_btn = tk.Button(
            buttons_frame,
            text="👥 Usuarios",
            command=self.open_user_management,
            bg='#3498db',
            fg='white',
            font=('Arial', 10),
            height=2
        )
        users_btn.pack(side=tk.LEFT, padx=5)
        
        config_btn = tk.Button(
            buttons_frame,
            text="⚙️ Config",
            command=self.open_configuration,
            bg='#9b59b6',
            fg='white',
            font=('Arial', 10),
            height=2
        )
        config_btn.pack(side=tk.LEFT, padx=5)
        
        main_btn = tk.Button(
            buttons_frame,
            text="🏠 Menú",
            command=self.open_main_window,
            bg='#2c3e50',
            fg='white',
            font=('Arial', 10),
            height=2
        )
        main_btn.pack(side=tk.LEFT, padx=5)
        
        close_btn = tk.Button(
            buttons_frame,
            text="Cerrar",
            command=self.root.destroy,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 12),
            height=2
        )
        close_btn.pack(side=tk.RIGHT)
    
    # === FUNCIONES DE BÚSQUEDA DE USUARIO ===
    
    def search_user_by_number(self, event=None):
        """Busca un usuario por número"""
        number_str = self.search_number_var.get().strip()
        if not number_str:
            return
        
        try:
            number = int(number_str)
            db = get_db_manager()
            user = db.buscar_usuario_por_numero(number)
            
            if user:
                self.load_user(user)
            else:
                messagebox.showinfo("No encontrado", f"No se encontró un usuario con el número {number}")
                
        except ValueError:
            messagebox.showwarning("Error", "El número debe ser un valor numérico")
    
    def on_name_search_change(self, event=None):
        """Maneja los cambios en la búsqueda por nombre"""
        name = self.search_name_var.get().strip()
        if len(name) < 2:
            self.name_suggestions.pack_forget()
            return
        
        try:
            db = get_db_manager()
            users = db.buscar_usuarios_por_nombre(name)
            
            if users:
                # Limpiar y llenar la lista de sugerencias
                self.name_suggestions.delete(0, tk.END)
                for user in users[:10]:  # Máximo 10 sugerencias
                    display_text = f"{user['numero']} - {user['nombre']} ({user['estado']})"
                    self.name_suggestions.insert(tk.END, display_text)
                    # Guardar el usuario completo como atributo del item
                    self.name_suggestions.insert(tk.END, "")
                    self.name_suggestions.delete(tk.END)
                
                # Guardar los usuarios para referencia
                self.suggestion_users = users[:10]
                
                # Mostrar la lista
                self.name_suggestions.pack(fill=tk.X, padx=10, pady=(0, 5))
            else:
                self.name_suggestions.pack_forget()
                
        except Exception as e:
            print(f"Error en búsqueda por nombre: {e}")
    
    def select_user_from_suggestions(self, event):
        """Selecciona un usuario de la lista de sugerencias"""
        selection = self.name_suggestions.curselection()
        if selection and hasattr(self, 'suggestion_users'):
            index = selection[0]
            if index < len(self.suggestion_users):
                user = self.suggestion_users[index]
                self.load_user(user)
                self.name_suggestions.pack_forget()
    
    def load_user(self, user: Dict):
        """Carga un usuario seleccionado"""
        if user['estado'] != 'Activo':
            messagebox.showwarning("Usuario Inactivo", 
                                 "Este usuario está marcado como 'Cancelado'. No se pueden registrar pagos.")
            return
        
        self.current_user = user
        
        # Actualizar información del usuario
        user_info = f"#{user['numero']} - {user['nombre']}"
        if user['direccion']:
            user_info += f" - {user['direccion']}"
        
        self.user_info_label.config(
            text=user_info,
            fg='#2c3e50'
        )
        
        # Limpiar campos de búsqueda
        self.search_number_var.set("")
        self.search_name_var.set("")
        self.name_suggestions.pack_forget()
        
        # Cargar meses pagados
        self.load_paid_months()
        
        # Habilitar procesamiento de pago
        self.update_payment_button_state()
    
    def load_paid_months(self):
        """Carga los meses ya pagados por el usuario"""
        if not self.current_user:
            return
        
        try:
            db = get_db_manager()
            self.paid_months = db.obtener_pagos_usuario_anio(self.current_user['id'], self.current_year)
            self.update_month_buttons()
        except Exception as e:
            print(f"Error al cargar meses pagados: {e}")
    
    # === FUNCIONES DE SELECCIÓN DE AÑO ===
    
    def prev_year(self):
        """Va al año anterior"""
        self.current_year -= 1
        self.year_label.config(text=str(self.current_year))
        self.load_paid_months()
        self.clear_month_selection()
    
    def next_year(self):
        """Va al año siguiente"""
        self.current_year += 1
        self.year_label.config(text=str(self.current_year))
        self.load_paid_months()
        self.clear_month_selection()
    
    # === FUNCIONES DE SELECCIÓN DE MESES ===
    
    def update_month_buttons(self):
        """Actualiza el estado visual de los botones de meses"""
        for month_num, button in self.month_buttons.items():
            if month_num in self.paid_months:
                # Mes ya pagado - verde oscuro, deshabilitado
                button.config(
                    bg='#27ae60',
                    fg='white',
                    state='disabled',
                    relief=tk.SUNKEN
                )
            elif month_num in self.selected_months:
                # Mes seleccionado para pagar - azul
                button.config(
                    bg='#3498db',
                    fg='white',
                    state='normal',
                    relief=tk.SUNKEN
                )
            else:
                # Mes disponible - gris claro
                button.config(
                    bg='#ecf0f1',
                    fg='#2c3e50',
                    state='normal',
                    relief=tk.RAISED
                )
    
    def toggle_month_selection(self, month_num: int):
        """Alterna la selección de un mes"""
        if month_num in self.paid_months:
            return  # No se puede seleccionar un mes ya pagado
        
        if month_num in self.selected_months:
            self.selected_months.remove(month_num)
        else:
            self.selected_months.append(month_num)
        
        self.selected_months.sort()
        self.update_month_buttons()
        self.update_totals()
        self.update_payment_button_state()
    
    def select_all_months(self):
        """Selecciona todos los meses disponibles (no pagados)"""
        self.selected_months = [m for m in range(1, 13) if m not in self.paid_months]
        self.update_month_buttons()
        self.update_totals()
        self.update_payment_button_state()
    
    def clear_month_selection(self):
        """Limpia la selección de meses"""
        self.selected_months = []
        self.update_month_buttons()
        self.update_totals()
        self.update_payment_button_state()
    
    # === FUNCIONES DE CONCEPTOS ADICIONALES ===
    
    def load_available_concepts(self):
        """Carga los conceptos de cobro disponibles"""
        try:
            db = get_db_manager()
            concepts = db.obtener_conceptos_cobro(solo_activos=True)
            
            concept_names = [concept['nombre'] for concept in concepts]
            self.concept_combo['values'] = concept_names
            
            # Guardar los conceptos para referencia
            self.available_concepts = {concept['nombre']: concept for concept in concepts}
            
        except Exception as e:
            print(f"Error al cargar conceptos: {e}")
    
    def on_concept_selected(self, event=None):
        """Maneja la selección de un concepto"""
        concept_name = self.concept_var.get()
        if concept_name in self.available_concepts:
            price = self.available_concepts[concept_name]['precio']
            self.concept_price_var.set(f"{price:.2f}")
    
    def add_additional_concept(self):
        """Agrega un concepto adicional al pago"""
        concept_name = self.concept_var.get().strip()
        price_str = self.concept_price_var.get().strip()
        
        if not concept_name or not price_str:
            messagebox.showwarning("Datos incompletos", "Seleccione un concepto y verifique el precio")
            return
        
        try:
            price = float(price_str)
            if price <= 0:
                messagebox.showwarning("Precio inválido", "El precio debe ser mayor a cero")
                return
        except ValueError:
            messagebox.showwarning("Precio inválido", "El precio debe ser un número válido")
            return
        
        # Agregar a la lista
        self.additional_concepts.append((concept_name, price))
        
        # Actualizar la lista visual
        display_text = f"{concept_name}: ${price:.2f}"
        self.concepts_listbox.insert(tk.END, display_text)
        
        # Limpiar campos
        self.concept_var.set("")
        self.concept_price_var.set("")
        
        # Actualizar totales
        self.update_totals()
        self.update_payment_button_state()
    
    def remove_selected_concept(self):
        """Elimina el concepto seleccionado de la lista"""
        selection = self.concepts_listbox.curselection()
        if not selection:
            messagebox.showinfo("Sin selección", "Seleccione un concepto para eliminar")
            return
        
        index = selection[0]
        
        # Eliminar de la lista de datos
        if 0 <= index < len(self.additional_concepts):
            del self.additional_concepts[index]
        
        # Eliminar de la lista visual
        self.concepts_listbox.delete(index)
        
        # Actualizar totales
        self.update_totals()
        self.update_payment_button_state()
    
    # === FUNCIONES DE CÁLCULOS ===
    
    def update_monthly_fee_display(self):
        """Actualiza la visualización de la cuota mensual"""
        try:
            db = get_db_manager()
            monthly_fee = db.obtener_configuracion('cuota_mensual')
            monthly_fee = float(monthly_fee) if monthly_fee else 50.0
            
            self.monthly_fee_label.config(text=f"Cuota mensual: ${monthly_fee:.2f}")
            self.monthly_fee = monthly_fee
            
        except Exception as e:
            self.monthly_fee = 50.0
            self.monthly_fee_label.config(text="Cuota mensual: $50.00")
    
    def update_totals(self):
        """Actualiza los totales de pago"""
        # Total mensualidades
        monthly_total = len(self.selected_months) * self.monthly_fee
        self.monthly_total_label.config(text=f"Mensualidades ({len(self.selected_months)} meses): ${monthly_total:.2f}")
        
        # Total conceptos adicionales
        concepts_total = sum(price for _, price in self.additional_concepts)
        self.concepts_total_label.config(text=f"Conceptos adicionales: ${concepts_total:.2f}")
        
        # Total general
        total = monthly_total + concepts_total
        self.total_label.config(text=f"TOTAL A PAGAR: ${total:.2f}")
    
    def update_payment_button_state(self):
        """Actualiza el estado del botón de procesar pago"""
        can_process = (
            self.current_user is not None and 
            (len(self.selected_months) > 0 or len(self.additional_concepts) > 0)
        )
        
        self.process_payment_btn.config(state='normal' if can_process else 'disabled')
    
    # === FUNCIONES DE PAGO ===
    
    def process_payment(self):
        """Procesa el pago"""
        if not self.current_user:
            messagebox.showerror("Error", "No hay usuario seleccionado")
            return
        
        if not self.selected_months and not self.additional_concepts:
            messagebox.showwarning("Sin conceptos", "No hay meses ni conceptos adicionales seleccionados")
            return
        
        # Confirmar pago
        monthly_total = len(self.selected_months) * self.monthly_fee
        concepts_total = sum(price for _, price in self.additional_concepts)
        total = monthly_total + concepts_total
        
        months_text = ", ".join([str(m) for m in self.selected_months]) if self.selected_months else "Ninguno"
        concepts_text = "\n".join([f"- {name}: ${price:.2f}" for name, price in self.additional_concepts])
        
        message = f"""¿Confirmar el pago?
        
Usuario: {self.current_user['nombre']} (#{self.current_user['numero']})
Año: {self.current_year}
        
Meses a pagar: {months_text}
Total mensualidades: ${monthly_total:.2f}

Conceptos adicionales:
{concepts_text if concepts_text else "Ninguno"}
Total conceptos: ${concepts_total:.2f}

TOTAL A PAGAR: ${total:.2f}"""
        
        if not messagebox.askyesno("Confirmar Pago", message):
            return
        
        try:
            # Registrar el pago en la base de datos
            db = get_db_manager()
            observations = self.observations_text.get("1.0", tk.END).strip()
            
            pago_id = db.registrar_pago(
                usuario_id=self.current_user['id'],
                meses_pagados=self.selected_months,
                anio=self.current_year,
                conceptos_adicionales=self.additional_concepts,
                observaciones=observations
            )
            
            if pago_id > 0:
                messagebox.showinfo("Éxito", f"Pago registrado correctamente.\nID de pago: {pago_id}")
                
                # Preguntar si desea generar recibo
                if messagebox.askyesno("Generar Recibo", "¿Desea generar e imprimir el recibo?"):
                    self.generate_receipt(pago_id)
                
                # Limpiar formulario
                self.load_paid_months()  # Recargar meses pagados
                self.clear_month_selection()
                self.additional_concepts = []
                self.concepts_listbox.delete(0, tk.END)
                self.observations_text.delete("1.0", tk.END)
                self.update_totals()
                
            else:
                messagebox.showerror("Error", "No se pudo registrar el pago")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar el pago: {str(e)}")
    
    def generate_receipt(self, pago_id: int):
        """Genera el recibo de pago"""
        try:
            from receipt_generator import ReceiptGenerator
            
            generator = ReceiptGenerator()
            pdf_path = generator.generate_receipt(pago_id)
            
            if pdf_path:
                # Preguntar si desea abrir el PDF
                if messagebox.askyesno("Recibo Generado", 
                                     f"Recibo guardado en:\n{pdf_path}\n\n¿Desea abrirlo?"):
                    import os
                    os.startfile(pdf_path)  # Windows
            
        except ImportError:
            messagebox.showinfo("Módulo no disponible", 
                               "El generador de recibos no está disponible aún")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar recibo: {str(e)}")
    
    def clear_all(self):
        """Limpia todo el formulario"""
        self.current_user = None
        self.paid_months = []
        self.selected_months = []
        self.additional_concepts = []
        
        # Limpiar interfaz
        self.user_info_label.config(
            text="No hay usuario seleccionado",
            fg='#7f8c8d'
        )
        
        self.search_number_var.set("")
        self.search_name_var.set("")
        self.name_suggestions.pack_forget()
        
        self.update_month_buttons()
        
        self.concepts_listbox.delete(0, tk.END)
        self.concept_var.set("")
        self.concept_price_var.set("")
        
        self.observations_text.delete("1.0", tk.END)
        
        self.update_totals()
        self.update_payment_button_state()
    
    # === FUNCIONES DE NAVEGACIÓN ===
    
    def open_user_management(self):
        """Abre el módulo de gestión de usuarios"""
        try:
            from user_management import UserManagementWindow
            UserManagementWindow(self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir gestión de usuarios: {str(e)}")
    
    def open_configuration(self):
        """Abre el módulo de configuración"""
        try:
            from configuration import ConfigurationWindow
            ConfigurationWindow(self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir configuración: {str(e)}")
    
    def open_main_window(self):
        """Abre la ventana principal"""
        try:
            # Cerrar esta ventana y abrir la principal
            self.root.destroy()
            from main import MainApplication
            app = MainApplication()
            app.run()
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir menú principal: {str(e)}")


def main():
    """Función principal para probar el módulo"""
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    
    app = PaymentRegistrationWindow()
    root.mainloop()


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de gestión de base de datos SQLite para el sistema de agua potable
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class DatabaseManager:
    def __init__(self, db_path: str = "agua_potable.db"):
        """
        Inicializa el gestor de base de datos
        
        Args:
            db_path: Ruta al archivo de la base de datos SQLite
        """
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """Obtiene una conexión a la base de datos"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Para obtener resultados como diccionarios
        return conn
    
    def init_database(self):
        """Inicializa las tablas de la base de datos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Tabla de usuarios
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero INTEGER UNIQUE NOT NULL,
                    nombre TEXT NOT NULL,
                    direccion TEXT,
                    telefono TEXT,
                    email TEXT,
                    estado TEXT DEFAULT 'Activo' CHECK (estado IN ('Activo', 'Cancelado')),
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de configuración del sistema
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS configuracion (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    clave TEXT UNIQUE NOT NULL,
                    valor TEXT NOT NULL,
                    descripcion TEXT,
                    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de conceptos de cobro
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conceptos_cobro (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL,
                    precio REAL NOT NULL,
                    activo BOOLEAN DEFAULT 1,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de pagos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pagos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER NOT NULL,
                    fecha_pago TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total REAL NOT NULL,
                    observaciones TEXT,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
                )
            ''')
            
            # Tabla detalle de pagos (mensualidades y otros conceptos)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS detalle_pagos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pago_id INTEGER NOT NULL,
                    concepto TEXT NOT NULL,
                    mes INTEGER NULL,  -- NULL para conceptos que no son mensualidades
                    anio INTEGER NOT NULL,
                    precio REAL NOT NULL,
                    cantidad INTEGER DEFAULT 1,
                    FOREIGN KEY (pago_id) REFERENCES pagos (id)
                )
            ''')
            
            # Insertar configuración inicial si no existe
            cursor.execute('''
                INSERT OR IGNORE INTO configuracion (clave, valor, descripcion)
                VALUES ('cuota_mensual', '50.0', 'Cuota mensual del servicio de agua')
            ''')
            
            cursor.execute('''
                INSERT OR IGNORE INTO configuracion (clave, valor, descripcion)
                VALUES ('pin_acceso', '1234', 'PIN de acceso al sistema')
            ''')
            
            # Insertar algunos conceptos de cobro predeterminados
            conceptos_default = [
                ('Cooperación Anual', 100.0),
                ('Toma Nueva', 500.0),
                ('Multa por Inasistencia', 25.0),
                ('Multa por Desperdicio', 75.0),
            ]
            
            for concepto, precio in conceptos_default:
                cursor.execute('''
                    INSERT OR IGNORE INTO conceptos_cobro (nombre, precio)
                    VALUES (?, ?)
                ''', (concepto, precio))
            
            conn.commit()
            
        except sqlite3.Error as e:
            print(f"Error al inicializar la base de datos: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    # === GESTIÓN DE USUARIOS ===
    
    def crear_usuario(self, numero: int, nombre: str, direccion: str = "", 
                     telefono: str = "", email: str = "") -> bool:
        """
        Crea un nuevo usuario
        
        Returns:
            bool: True si se creó exitosamente, False si ya existe el número
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO usuarios (numero, nombre, direccion, telefono, email)
                VALUES (?, ?, ?, ?, ?)
            ''', (numero, nombre, direccion, telefono, email))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # El número ya existe
        finally:
            conn.close()
    
    def get_next_user_number(self) -> int:
        """
        Obtiene el siguiente número de usuario disponible
        
        Returns:
            int: El siguiente número secuencial disponible
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Buscar el número más alto
            cursor.execute('SELECT MAX(numero) FROM usuarios')
            result = cursor.fetchone()
            max_number = result[0] if result and result[0] is not None else 0
            return max_number + 1
        finally:
            conn.close()
    
    def buscar_usuario_por_numero(self, numero: int) -> Optional[Dict]:
        """Busca un usuario por su número"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM usuarios WHERE numero = ?', (numero,))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()
    
    def buscar_usuarios_por_nombre(self, nombre: str) -> List[Dict]:
        """Busca usuarios por nombre (búsqueda parcial)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT * FROM usuarios 
                WHERE nombre LIKE ? 
                ORDER BY nombre
            ''', (f'%{nombre}%',))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()
    
    def actualizar_usuario(self, usuario_id: int, **kwargs) -> bool:
        """Actualiza los datos de un usuario"""
        if not kwargs:
            return False
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Construir la consulta dinámicamente
            campos = list(kwargs.keys())
            valores = list(kwargs.values())
            valores.append(usuario_id)
            
            set_clause = ', '.join([f"{campo} = ?" for campo in campos])
            
            cursor.execute(f'''
                UPDATE usuarios 
                SET {set_clause}
                WHERE id = ?
            ''', valores)
            
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    def cambiar_estado_usuario(self, usuario_id: int, estado: str) -> bool:
        """Cambia el estado de un usuario (Activo/Cancelado)"""
        if estado not in ['Activo', 'Cancelado']:
            return False
        return self.actualizar_usuario(usuario_id, estado=estado)
    
    def obtener_todos_usuarios(self, solo_activos: bool = False) -> List[Dict]:
        """Obtiene todos los usuarios"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if solo_activos:
                cursor.execute('''
                    SELECT * FROM usuarios 
                    WHERE estado = 'Activo' 
                    ORDER BY numero
                ''')
            else:
                cursor.execute('SELECT * FROM usuarios ORDER BY numero')
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()
    
    # === GESTIÓN DE PAGOS ===
    
    def obtener_pagos_usuario_anio(self, usuario_id: int, anio: int) -> List[int]:
        """
        Obtiene los meses pagados por un usuario en un año específico
        
        Returns:
            List[int]: Lista de meses pagados (1-12)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT DISTINCT mes 
                FROM detalle_pagos dp
                JOIN pagos p ON dp.pago_id = p.id
                WHERE p.usuario_id = ? AND dp.anio = ? AND dp.mes IS NOT NULL
                ORDER BY mes
            ''', (usuario_id, anio))
            
            rows = cursor.fetchall()
            return [row[0] for row in rows]
        finally:
            conn.close()
    
    def registrar_pago(self, usuario_id: int, meses_pagados: List[int], anio: int,
                      conceptos_adicionales: List[Tuple[str, float]] = None,
                      observaciones: str = "") -> int:
        """
        Registra un pago completo
        
        Args:
            usuario_id: ID del usuario
            meses_pagados: Lista de meses pagados (1-12)
            anio: Año de los meses pagados
            conceptos_adicionales: Lista de tuplas (concepto, precio)
            observaciones: Observaciones del pago
            
        Returns:
            int: ID del pago registrado, 0 si hay error
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Obtener la cuota mensual actual
            cuota_mensual = self.obtener_configuracion('cuota_mensual')
            cuota_mensual = float(cuota_mensual) if cuota_mensual else 50.0
            
            # Calcular total
            total = len(meses_pagados) * cuota_mensual
            if conceptos_adicionales:
                total += sum(precio for _, precio in conceptos_adicionales)
            
            # Insertar el pago principal
            cursor.execute('''
                INSERT INTO pagos (usuario_id, total, observaciones)
                VALUES (?, ?, ?)
            ''', (usuario_id, total, observaciones))
            
            pago_id = cursor.lastrowid
            
            # Insertar detalles de mensualidades
            for mes in meses_pagados:
                cursor.execute('''
                    INSERT INTO detalle_pagos (pago_id, concepto, mes, anio, precio)
                    VALUES (?, ?, ?, ?, ?)
                ''', (pago_id, 'Mensualidad', mes, anio, cuota_mensual))
            
            # Insertar conceptos adicionales
            if conceptos_adicionales:
                for concepto, precio in conceptos_adicionales:
                    cursor.execute('''
                        INSERT INTO detalle_pagos (pago_id, concepto, mes, anio, precio)
                        VALUES (?, ?, NULL, ?, ?)
                    ''', (pago_id, concepto, anio, precio))
            
            conn.commit()
            return pago_id
            
        except sqlite3.Error as e:
            print(f"Error al registrar pago: {e}")
            conn.rollback()
            return 0
        finally:
            conn.close()
    
    def obtener_historial_pagos_usuario(self, usuario_id: int) -> List[Dict]:
        """Obtiene el historial de pagos de un usuario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT p.*, u.nombre, u.numero
                FROM pagos p
                JOIN usuarios u ON p.usuario_id = u.id
                WHERE p.usuario_id = ?
                ORDER BY p.fecha_pago DESC
            ''', (usuario_id,))
            
            rows = cursor.fetchall()
            pagos = [dict(row) for row in rows]
            
            # Obtener detalles de cada pago
            for pago in pagos:
                cursor.execute('''
                    SELECT * FROM detalle_pagos 
                    WHERE pago_id = ?
                    ORDER BY mes
                ''', (pago['id'],))
                
                detalles = cursor.fetchall()
                pago['detalles'] = [dict(detalle) for detalle in detalles]
            
            return pagos
        finally:
            conn.close()
    
    def obtener_detalle_pago(self, pago_id: int) -> Dict:
        """Obtiene el detalle completo de un pago para generar recibo"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Obtener información del pago y usuario
            cursor.execute('''
                SELECT p.*, u.nombre, u.numero, u.direccion
                FROM pagos p
                JOIN usuarios u ON p.usuario_id = u.id
                WHERE p.id = ?
            ''', (pago_id,))
            
            pago_row = cursor.fetchone()
            if not pago_row:
                return {}
            
            pago = dict(pago_row)
            
            # Obtener detalles del pago
            cursor.execute('''
                SELECT * FROM detalle_pagos 
                WHERE pago_id = ?
                ORDER BY mes, concepto
            ''', (pago_id,))
            
            detalles = cursor.fetchall()
            pago['detalles'] = [dict(detalle) for detalle in detalles]
            
            return pago
        finally:
            conn.close()
    
    # === GESTIÓN DE CONFIGURACIÓN ===
    
    def obtener_configuracion(self, clave: str) -> Optional[str]:
        """Obtiene un valor de configuración"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT valor FROM configuracion WHERE clave = ?', (clave,))
            row = cursor.fetchone()
            return row[0] if row else None
        finally:
            conn.close()
    
    def actualizar_configuracion(self, clave: str, valor: str) -> bool:
        """Actualiza un valor de configuración"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE configuracion 
                SET valor = ?, fecha_modificacion = CURRENT_TIMESTAMP
                WHERE clave = ?
            ''', (valor, clave))
            
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    def verificar_pin(self, pin: str) -> bool:
        """Verifica si el PIN ingresado es correcto"""
        pin_actual = self.obtener_configuracion('pin_acceso')
        return pin_actual == pin
    
    # === GESTIÓN DE CONCEPTOS DE COBRO ===
    
    def obtener_conceptos_cobro(self, solo_activos: bool = True) -> List[Dict]:
        """Obtiene todos los conceptos de cobro"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if solo_activos:
                cursor.execute('''
                    SELECT * FROM conceptos_cobro 
                    WHERE activo = 1 
                    ORDER BY nombre
                ''')
            else:
                cursor.execute('SELECT * FROM conceptos_cobro ORDER BY nombre')
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()
    
    def crear_concepto_cobro(self, nombre: str, precio: float) -> bool:
        """Crea un nuevo concepto de cobro"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO conceptos_cobro (nombre, precio)
                VALUES (?, ?)
            ''', (nombre, precio))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Ya existe
        finally:
            conn.close()
    
    def actualizar_concepto_cobro(self, concepto_id: int, nombre: str = None, 
                                 precio: float = None, activo: bool = None) -> bool:
        """Actualiza un concepto de cobro"""
        campos_actualizar = {}
        
        if nombre is not None:
            campos_actualizar['nombre'] = nombre
        if precio is not None:
            campos_actualizar['precio'] = precio
        if activo is not None:
            campos_actualizar['activo'] = 1 if activo else 0
        
        if not campos_actualizar:
            return False
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            campos = list(campos_actualizar.keys())
            valores = list(campos_actualizar.values())
            valores.append(concepto_id)
            
            set_clause = ', '.join([f"{campo} = ?" for campo in campos])
            
            cursor.execute(f'''
                UPDATE conceptos_cobro 
                SET {set_clause}
                WHERE id = ?
            ''', valores)
            
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    def eliminar_concepto_cobro(self, concepto_id: int) -> bool:
        """Desactiva un concepto de cobro (no lo elimina físicamente)"""
        return self.actualizar_concepto_cobro(concepto_id, activo=False)


# Función de utilidad para obtener una instancia global del gestor
_db_manager = None

def get_db_manager() -> DatabaseManager:
    """Obtiene una instancia global del gestor de base de datos"""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager
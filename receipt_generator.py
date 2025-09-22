#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de recibos de pago para el sistema de agua potable
"""

import os
from datetime import datetime
from typing import Dict, Optional
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from database import get_db_manager

class ReceiptGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.create_custom_styles()
        
        # Configurar directorios
        self.receipts_dir = "recibos"
        self.ensure_directories()
    
    def create_custom_styles(self):
        """Crea estilos personalizados para el recibo"""
        # Estilo para el título
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=6,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        # Estilo para subtítulos
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceAfter=12,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        # Estilo para información del usuario
        self.user_info_style = ParagraphStyle(
            'UserInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_LEFT
        )
        
        # Estilo para totales
        self.total_style = ParagraphStyle(
            'Total',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=6,
            alignment=TA_RIGHT,
            textColor=colors.darkgreen
        )
        
        # Estilo para el pie de página
        self.footer_style = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
    
    def ensure_directories(self):
        """Asegura que existan los directorios necesarios"""
        if not os.path.exists(self.receipts_dir):
            os.makedirs(self.receipts_dir)
    
    def generate_receipt(self, pago_id: int) -> Optional[str]:
        """
        Genera un recibo de pago en PDF
        
        Args:
            pago_id: ID del pago para generar el recibo
            
        Returns:
            str: Ruta del archivo PDF generado, None si hay error
        """
        try:
            # Obtener datos del pago
            db = get_db_manager()
            pago_data = db.obtener_detalle_pago(pago_id)
            
            if not pago_data:
                print(f"No se encontró el pago con ID {pago_id}")
                return None
            
            # Generar nombre del archivo
            fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recibo_{pago_data['numero']}_{fecha}.pdf"
            filepath = os.path.join(self.receipts_dir, filename)
            
            # Crear el documento PDF
            doc = SimpleDocTemplate(
                filepath,
                pagesize=letter,
                rightMargin=inch,
                leftMargin=inch,
                topMargin=inch,
                bottomMargin=inch
            )
            
            # Construir el contenido del recibo
            story = []
            story.extend(self.build_header(pago_data))
            story.extend(self.build_user_info(pago_data))
            story.extend(self.build_payment_details(pago_data))
            story.extend(self.build_totals(pago_data))
            story.extend(self.build_footer(pago_data))
            
            # Generar el PDF
            doc.build(story)
            
            return filepath
            
        except Exception as e:
            print(f"Error al generar recibo: {e}")
            return None
    
    def build_header(self, pago_data: Dict) -> list:
        """Construye el encabezado del recibo"""
        elements = []
        
        # Intentar cargar el logo
        logo_path = "logo.jpg"
        if os.path.exists(logo_path):
            try:
                logo = Image(logo_path, width=60, height=60)
                elements.append(logo)
                elements.append(Spacer(1, 10))
            except:
                pass  # Si no se puede cargar, continuar sin logo
        
        # Título principal
        title = Paragraph("COMITÉ DE AGUA POTABLE", self.title_style)
        elements.append(title)
        
        # Subtítulo
        subtitle = Paragraph("RECIBO DE PAGO", self.subtitle_style)
        elements.append(subtitle)
        
        elements.append(Spacer(1, 20))
        
        return elements
    
    def build_user_info(self, pago_data: Dict) -> list:
        """Construye la información del usuario"""
        elements = []
        
        # Información del recibo y usuario
        fecha_pago = datetime.strptime(pago_data['fecha_pago'], '%Y-%m-%d %H:%M:%S')
        fecha_str = fecha_pago.strftime('%d/%m/%Y %H:%M')
        
        info_data = [
            ['Recibo No.:', str(pago_data['id']), 'Fecha:', fecha_str],
            ['Usuario No.:', str(pago_data['numero']), 'Nombre:', pago_data['nombre']],
            ['Dirección:', pago_data['direccion'] or 'No especificada', '', '']
        ]
        
        info_table = Table(info_data, colWidths=[80, 120, 60, 120])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),  # Primera columna en bold
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),  # Tercera columna en bold
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def build_payment_details(self, pago_data: Dict) -> list:
        """Construye los detalles del pago"""
        elements = []
        
        # Título de la tabla
        details_title = Paragraph("DETALLE DEL PAGO", self.subtitle_style)
        elements.append(details_title)
        elements.append(Spacer(1, 10))
        
        # Preparar datos para la tabla
        table_data = [['Concepto', 'Mes/Año', 'Precio', 'Cantidad', 'Subtotal']]
        
        # Agrupar detalles por tipo
        mensualidades = []
        otros_conceptos = []
        
        for detalle in pago_data['detalles']:
            if detalle['mes']:
                mensualidades.append(detalle)
            else:
                otros_conceptos.append(detalle)
        
        # Agregar mensualidades
        if mensualidades:
            # Ordenar por mes
            mensualidades.sort(key=lambda x: x['mes'])
            
            for detalle in mensualidades:
                mes_nombre = self.get_month_name(detalle['mes'])
                table_data.append([
                    'Cuota Mensual',
                    f"{mes_nombre} {detalle['anio']}",
                    f"${detalle['precio']:.2f}",
                    str(detalle['cantidad']),
                    f"${detalle['precio'] * detalle['cantidad']:.2f}"
                ])
        
        # Agregar otros conceptos
        for detalle in otros_conceptos:
            table_data.append([
                detalle['concepto'],
                str(detalle['anio']),
                f"${detalle['precio']:.2f}",
                str(detalle['cantidad']),
                f"${detalle['precio'] * detalle['cantidad']:.2f}"
            ])
        
        # Crear la tabla
        details_table = Table(table_data, colWidths=[150, 80, 80, 60, 80])
        details_table.setStyle(TableStyle([
            # Estilo del encabezado
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Estilo del contenido
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),    # Concepto alineado a la izquierda
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'), # Resto centrado
            ('ALIGN', (-1, 1), (-1, -1), 'RIGHT'), # Subtotal alineado a la derecha
            
            # Bordes
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            
            # Padding
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            
            # Alternar colores de fila
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        elements.append(details_table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def build_totals(self, pago_data: Dict) -> list:
        """Construye la sección de totales"""
        elements = []
        
        # Calcular totales por categoría
        total_mensualidades = 0
        total_otros = 0
        
        for detalle in pago_data['detalles']:
            subtotal = detalle['precio'] * detalle['cantidad']
            if detalle['mes']:
                total_mensualidades += subtotal
            else:
                total_otros += subtotal
        
        # Crear tabla de totales
        totals_data = []
        
        if total_mensualidades > 0:
            totals_data.append(['Subtotal Mensualidades:', f"${total_mensualidades:.2f}"])
        
        if total_otros > 0:
            totals_data.append(['Subtotal Otros Conceptos:', f"${total_otros:.2f}"])
        
        totals_data.append(['', ''])  # Línea en blanco
        totals_data.append(['TOTAL A PAGAR:', f"${pago_data['total']:.2f}"])
        
        # Crear tabla
        totals_table = Table(totals_data, colWidths=[300, 100])
        totals_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -2), 'Helvetica'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -2), 10),
            ('FONTSIZE', (0, -1), (-1, -1), 14),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.darkgreen),
            ('LINEABOVE', (0, -1), (-1, -1), 2, colors.darkgreen),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        elements.append(totals_table)
        elements.append(Spacer(1, 30))
        
        return elements
    
    def build_footer(self, pago_data: Dict) -> list:
        """Construye el pie del recibo"""
        elements = []
        
        # Observaciones si las hay
        if pago_data.get('observaciones'):
            obs_title = Paragraph("OBSERVACIONES:", self.subtitle_style)
            elements.append(obs_title)
            
            obs_text = Paragraph(pago_data['observaciones'], self.user_info_style)
            elements.append(obs_text)
            elements.append(Spacer(1, 20))
        
        # Línea de firma
        elements.append(Spacer(1, 30))
        
        signature_line = Table([['_' * 50]], colWidths=[300])
        signature_line.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))
        elements.append(signature_line)
        
        signature_text = Paragraph("Firma del Cobrador", self.user_info_style)
        elements.append(signature_text)
        
        elements.append(Spacer(1, 20))
        
        # Pie de página
        footer_text = Paragraph(
            f"Recibo generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}",
            self.footer_style
        )
        elements.append(footer_text)
        
        return elements
    
    def get_month_name(self, month_num: int) -> str:
        """Convierte número de mes a nombre"""
        months = [
            '', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
        ]
        return months[month_num] if 1 <= month_num <= 12 else str(month_num)
    
    def print_receipt(self, filepath: str) -> bool:
        """
        Intenta imprimir el recibo (Windows)
        
        Args:
            filepath: Ruta del archivo PDF
            
        Returns:
            bool: True si se inició la impresión correctamente
        """
        try:
            import os
            os.startfile(filepath, "print")
            return True
        except Exception as e:
            print(f"Error al imprimir: {e}")
            return False


def main():
    """Función de prueba"""
    generator = ReceiptGenerator()
    
    # Crear un pago de prueba
    db = get_db_manager()
    
    # Verificar si hay usuarios para hacer una prueba
    usuarios = db.obtener_todos_usuarios()
    if not usuarios:
        print("No hay usuarios en la base de datos para hacer prueba")
        return
    
    # Usar el primer usuario
    usuario = usuarios[0]
    
    # Registrar un pago de prueba
    pago_id = db.registrar_pago(
        usuario_id=usuario['id'],
        meses_pagados=[1, 2, 3],
        anio=2024,
        conceptos_adicionales=[("Cooperación Anual", 100.0)],
        observaciones="Pago de prueba del sistema"
    )
    
    if pago_id > 0:
        print(f"Pago de prueba registrado con ID: {pago_id}")
        
        # Generar recibo
        pdf_path = generator.generate_receipt(pago_id)
        if pdf_path:
            print(f"Recibo generado: {pdf_path}")
        else:
            print("Error al generar recibo")
    else:
        print("Error al registrar pago de prueba")


if __name__ == "__main__":
    main()
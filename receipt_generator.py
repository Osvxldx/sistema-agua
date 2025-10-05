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
        """Crea estilos personalizados mejorados para el recibo"""
        # Estilo para el título principal - más prominente
        self.title_style = ParagraphStyle(
            'ProfessionalTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            spaceAfter=8,
            spaceBefore=8,
            alignment=TA_CENTER,
            textColor=colors.Color(0.12, 0.23, 0.54),  # Azul profesional
            fontName='Helvetica-Bold'
        )
        
        # Estilo para subtítulos - más elegante
        self.subtitle_style = ParagraphStyle(
            'ProfessionalSubtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=6,
            alignment=TA_CENTER,
            textColor=colors.Color(0.2, 0.4, 0.8),  # Azul claro
            fontName='Helvetica-Bold'
        )
        
        # Estilo para información de la empresa
        self.company_style = ParagraphStyle(
            'CompanyInfo',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=4,
            alignment=TA_CENTER,
            textColor=colors.Color(0.2, 0.2, 0.2),
            fontName='Helvetica'
        )
        
        # Estilo para información del usuario - más profesional
        self.user_info_style = ParagraphStyle(
            'ProfessionalUserInfo',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            spaceBefore=2,
            alignment=TA_LEFT,
            textColor=colors.Color(0.1, 0.1, 0.1),
            fontName='Helvetica'
        )
        
        # Estilo para títulos de sección
        self.section_title_style = ParagraphStyle(
            'SectionTitle',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=8,
            spaceBefore=12,
            alignment=TA_LEFT,
            textColor=colors.Color(0.12, 0.23, 0.54),
            fontName='Helvetica-Bold'
        )
        
        # Estilo para totales - más destacado
        self.total_style = ParagraphStyle(
            'ProfessionalTotal',
            parent=self.styles['Normal'],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=8,
            alignment=TA_RIGHT,
            textColor=colors.Color(0.0, 0.5, 0.0),  # Verde profesional
            fontName='Helvetica-Bold'
        )
        
        # Estilo para el pie de página mejorado
        self.footer_style = ParagraphStyle(
            'ProfessionalFooter',
            parent=self.styles['Normal'],
            fontSize=9,
            alignment=TA_CENTER,
            textColor=colors.Color(0.4, 0.4, 0.4),
            fontName='Helvetica-Oblique'
        )
        
        # Estilo para números de recibo
        self.receipt_number_style = ParagraphStyle(
            'ReceiptNumber',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_RIGHT,
            textColor=colors.Color(0.6, 0.0, 0.0),  # Rojo oscuro
            fontName='Helvetica-Bold'
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
        """Construye el encabezado profesional del recibo"""
        elements = []
        
        # Crear tabla para header con logo y información de empresa
        header_data = []
        
        # Intentar cargar el logo más grande y visible
        logo_path = "logo.jpg"
        logo_cell = ""
        if os.path.exists(logo_path):
            try:
                logo = Image(logo_path, width=80, height=80)
                logo_cell = logo
            except:
                logo_cell = Paragraph("LOGO", self.company_style)
        else:
            logo_cell = Paragraph("AGUA<br/>POTABLE", self.company_style)
        
        # Información de la empresa
        company_info = [
            Paragraph("<b>COMITÉ DE AGUA POTABLE</b>", self.title_style),
            Paragraph("Sistema de Gestión Profesional", self.company_style),
            Paragraph("📍 Dirección del Comité", self.company_style),
            Paragraph("📞 Teléfono de Contacto", self.company_style),
            Paragraph("📧 correo@comiteagua.com", self.company_style)
        ]
        
        # Información del recibo
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        recibo_info = [
            Paragraph(f"<b>RECIBO DE PAGO</b>", self.subtitle_style),
            Paragraph(f"N° Recibo: {pago_data.get('id', 'N/A')}", self.receipt_number_style),
            Paragraph(f"Fecha: {fecha_actual}", self.receipt_number_style),
            Paragraph(f"Usuario: {pago_data.get('numero', 'N/A')}", self.receipt_number_style)
        ]
        
        # Crear la tabla del header
        header_table_data = [
            [logo_cell, company_info[0], recibo_info[0]],
            ["", company_info[1], recibo_info[1]],
            ["", company_info[2], recibo_info[2]],
            ["", company_info[3], recibo_info[3]],
            ["", company_info[4], recibo_info[4]]
        ]
        
        header_table = Table(header_table_data, colWidths=[1.5*inch, 3*inch, 2*inch])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LINEBELOW', (0, 4), (-1, 4), 2, colors.Color(0.12, 0.23, 0.54)),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(header_table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def build_user_info(self, pago_data: Dict) -> list:
        """Construye la información del usuario de forma profesional"""
        elements = []
        
        # Título de sección
        section_title = Paragraph("INFORMACIÓN DEL CLIENTE", self.section_title_style)
        elements.append(section_title)
        
        # Información del usuario en formato de tabla profesional
        fecha_pago = datetime.strptime(pago_data['fecha_pago'], '%Y-%m-%d %H:%M:%S')
        fecha_str = fecha_pago.strftime('%d de %B de %Y - %H:%M')
        
        # Crear tabla de información del usuario
        user_info_data = [
            ['👤 Nombre del Cliente:', pago_data['nombre']],
            ['🏠 N° de Usuario:', str(pago_data['numero'])],
            ['📍 Dirección:', pago_data['direccion'] or 'No especificada'],
            ['📅 Fecha de Pago:', fecha_str],
            ['💳 Estado:', 'ACTIVO' if pago_data.get('estado') == 'activo' else 'CANCELADO']
        ]
        
        # Crear tabla profesional para información del usuario
        user_table = Table(user_info_data, colWidths=[2*inch, 4*inch])
        user_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LINEBELOW', (0, 0), (-1, -1), 1, colors.Color(0.8, 0.8, 0.8)),
            ('BACKGROUND', (0, 0), (-1, -1), colors.Color(0.98, 0.98, 0.98)),
        ]))
        
        elements.append(user_table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def build_payment_details(self, pago_data: Dict) -> list:
        """
        Builds the payment details section for the receipt with a professional design.

        Args:
            pago_data (Dict): A dictionary containing payment information. It must include a 'detalles' key,
                which is a list of dictionaries. Each dictionary in 'detalles' should have the following keys:
                - 'mes' (int or None): The month number if applicable, or None for other concepts.
                - 'anio' (int): The year of the payment.
                - 'precio' (float): The unit price of the service or concept.
                - 'cantidad' (int): The quantity paid for.
                - 'concepto' (str): The name of the concept or service.

        Returns:
            list: A list of ReportLab flowable elements (Paragraph, Spacer, Table, etc.) representing
                the payment details section to be added to the PDF document.
        """
        elements = []
        
        # Título de la sección
        details_title = Paragraph("💰 DETALLE DE SERVICIOS PAGADOS", self.section_title_style)
        elements.append(details_title)
        elements.append(Spacer(1, 12))
        
        # Preparar datos para la tabla con mejor formato
        table_data = [['CONCEPTO', 'PERÍODO', 'PRECIO UNIT.', 'CANT.', 'SUBTOTAL']]
        
        # Agrupar detalles por tipo
        mensualidades = []
        otros_conceptos = []
        
        for detalle in pago_data['detalles']:
            if detalle['mes']:
                mensualidades.append(detalle)
            else:
                otros_conceptos.append(detalle)
        
        # Agregar mensualidades con mejor formato
        if mensualidades:
            mensualidades.sort(key=lambda x: x['mes'])
            
            for detalle in mensualidades:
                mes_nombre = self.get_month_name(detalle['mes'])
                table_data.append([
                    'Servicio de Agua Potable',
                    f"{mes_nombre} {detalle['anio']}",
                    f"$ {detalle['precio']:.2f}",
                    str(detalle['cantidad']),
                    f"$ {detalle['precio'] * detalle['cantidad']:.2f}"
                ])
        
        # Agregar otros conceptos con iconos
        for detalle in otros_conceptos:
            icono = self.get_concept_icon(detalle['concepto'])
            table_data.append([
                f"{icono} {detalle['concepto']}",
                str(detalle['anio']),
                f"$ {detalle['precio']:.2f}",
                str(detalle['cantidad']),
                f"$ {detalle['precio'] * detalle['cantidad']:.2f}"
            ])
        
        # Crear la tabla profesional
        details_table = Table(table_data, colWidths=[2.5*inch, 1.2*inch, 0.8*inch, 0.5*inch, 1*inch])
        details_table.setStyle(TableStyle([
            # Estilo del encabezado mejorado
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.12, 0.23, 0.54)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Estilo del contenido
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),    # Concepto
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),  # Período
            ('ALIGN', (2, 1), (2, -1), 'RIGHT'),   # Precio
            ('ALIGN', (3, 1), (3, -1), 'CENTER'),  # Cantidad
            ('ALIGN', (4, 1), (4, -1), 'RIGHT'),   # Subtotal
            
            # Bordes profesionales
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.Color(0.12, 0.23, 0.54)),
            ('LINEBELOW', (0, 1), (-1, -1), 0.5, colors.Color(0.8, 0.8, 0.8)),
            ('LINEBEFORE', (1, 0), (-1, -1), 0.5, colors.Color(0.9, 0.9, 0.9)),
            
            # Padding mejorado
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            
            # Colores alternados más suaves
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.97, 0.97, 0.97)]),
        ]))
        
        elements.append(details_table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def get_concept_icon(self, concepto: str) -> str:
        """Obtiene el icono apropiado para un concepto"""
        concepto_lower = concepto.lower()
        if 'reconexión' in concepto_lower or 'reconexion' in concepto_lower:
            return '🔧'
        elif 'multa' in concepto_lower:
            return '⚠️'
        elif 'cooperación' in concepto_lower:
            return '🤝'
        elif 'instalación' in concepto_lower:
            return '🏗️'
        elif 'mantenimiento' in concepto_lower:
            return '🛠️'
        else:
            return '📋'
    
    def build_totals(self, pago_data: Dict) -> list:
        """Construye la sección de totales con diseño profesional"""
        elements = []
        
        elements.append(Spacer(1, 15))
        
        # Calcular totales por categoría
        total_mensualidades = 0
        total_otros = 0
        
        for detalle in pago_data['detalles']:
            subtotal = detalle['precio'] * detalle['cantidad']
            if detalle['mes']:
                total_mensualidades += subtotal
            else:
                total_otros += subtotal
        
        # Crear tabla de totales profesional
        totals_data = []
        
        if total_mensualidades > 0:
            totals_data.append(['🚰 Subtotal Servicios Mensuales:', f"$ {total_mensualidades:.2f}"])
        
        if total_otros > 0:
            totals_data.append(['📋 Subtotal Otros Conceptos:', f"$ {total_otros:.2f}"])
        
        # Línea separadora
        totals_data.append(['─────────────────────────────────────', '─────────────'])
        
        # Total principal destacado
        totals_data.append(['💰 TOTAL PAGADO:', f"$ {pago_data['total']:.2f}"])
        
        # Crear tabla con mejor diseño
        totals_table = Table(totals_data, colWidths=[4*inch, 1.5*inch])
        totals_table.setStyle(TableStyle([
            # Subtotales
            ('FONTNAME', (0, 0), (-1, -3), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -3), 11),
            ('TEXTCOLOR', (0, 0), (-1, -3), colors.Color(0.2, 0.2, 0.2)),
            
            # Línea separadora
            ('FONTNAME', (0, -2), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, -2), (-1, -2), 8),
            ('TEXTCOLOR', (0, -2), (-1, -2), colors.Color(0.5, 0.5, 0.5)),
            
            # Total principal
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 16),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.Color(0.0, 0.5, 0.0)),
            ('BACKGROUND', (0, -1), (-1, -1), colors.Color(0.95, 1.0, 0.95)),
            
            # Alineación
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.darkgreen),
            ('LINEABOVE', (0, -1), (-1, -1), 2, colors.darkgreen),
            # Padding mejorado
            ('TOPPADDING', (0, 0), (-1, -2), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -2), 6),
            ('TOPPADDING', (0, -1), (-1, -1), 12),
            ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ]))
        
        elements.append(totals_table)
        elements.append(Spacer(1, 25))
        
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
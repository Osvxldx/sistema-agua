# Sistema de Gestión de Agua Potable

Sistema completo para la administración de comités de agua potable desarrollado en Python.

## Características Principales

### 🔐 Seguridad
- Sistema de autenticación con PIN (por defecto: 1234)
- Configuración protegida con verificación de PIN
- Respaldos de base de datos

### 👥 Gestión de Usuarios
- Registro completo de usuarios (número, nombre, dirección, teléfono, email)
- Búsqueda por número o nombre
- Estado de usuario (Activo/Cancelado)
- Historial de pagos por usuario

### 💰 Registro de Pagos
- Interfaz visual con calendario de 12 meses
- Cálculo automático de totales
- Conceptos adicionales de cobro (cooperaciones, multas, etc.)
- Generación automática de recibos en PDF
- Observaciones por pago

### 🧾 Generación de Recibos
- Recibos profesionales en formato PDF
- Desglose detallado de conceptos pagados
- Logo personalizable
- Opción de impresión directa

### ⚙️ Configuración del Sistema
- Gestión de cuota mensual
- Administración de conceptos de cobro
- Información del comité
- Cambio de PIN de seguridad
- Respaldo y restauración de datos

### 📊 Base de Datos
- SQLite integrada (sin necesidad de servidor)
- Historial completo de transacciones
- Integridad referencial
- Consultas optimizadas

## Requisitos del Sistema

- **Sistema Operativo:** Windows 7 o superior
- **Python:** 3.8 o superior (incluido en la instalación)
- **Memoria RAM:** Mínimo 2GB
- **Espacio en disco:** 100MB libres
- **Pantalla:** Resolución mínima 1024x768

## Instalación

### Opción 1: Instalación Automática (Recomendada)

1. Descargar todos los archivos en una carpeta
2. Ejecutar `install.bat` como administrador
3. Seguir las instrucciones en pantalla

### Opción 2: Instalación Manual

1. Instalar Python 3.8+ desde [python.org](https://python.org)
2. Abrir terminal/CMD en la carpeta del sistema
3. Ejecutar:
   ```
   pip install reportlab Pillow python-dateutil
   ```
4. Ejecutar el sistema:
   ```
   python main.py
   ```

## Estructura de Archivos

```
sistema-agua-potable/
├── main.py                 # Aplicación principal
├── auth.py                 # Sistema de autenticación
├── database.py             # Gestor de base de datos
├── user_management.py      # Módulo de usuarios
├── payment_registration.py # Módulo de pagos
├── receipt_generator.py    # Generador de recibos
├── configuration.py        # Configuración del sistema
├── csv_importer.py         # Importador de datos CSV
├── logo.jpg               # Logo del comité
├── ejemplo.jpg            # Imagen de ejemplo
├── install.bat            # Instalador automático
├── README.md              # Este archivo
├── GUIA_GITHUB.txt        # Guía de Git y GitHub
└── recibos/               # Carpeta de recibos generados
```

## Primer Uso

1. **Iniciar el sistema:** Ejecutar `main.py`
2. **Ingresar PIN:** Usar `1234` (PIN por defecto)
3. **Configurar sistema:**
   - Ir a "Configuración del Sistema"
   - Actualizar información del comité
   - Ajustar cuota mensual
   - Cambiar PIN de acceso (recomendado)
4. **Cargar usuarios:**
   - Usar "Gestión de Usuarios" para agregar usuarios manualmente
   - O usar `csv_importer.py` para importar desde CSV

## Importación de Datos CSV

### Formato para Usuarios (BASE DE DATOS.csv)
```csv
numero,nombre,direccion,telefono,email
1,Juan Pérez,Calle 123,555-1234,juan@email.com
2,María García,Av. Central 456,555-5678,maria@email.com
```

### Formato para Pagos (PAGOS XXXX.csv)
```csv
numero,1,2,3,4,5,6,7,8,9,10,11,12
1,X,X,X,,X,X,X,X,X,X,X,X
2,X,X,,X,X,X,X,X,X,X,X,X
```
*X = mes pagado, vacío = mes no pagado*

## Uso del Sistema

### Módulo de Gestión de Usuarios
1. **Nuevo Usuario:** Botón "Nuevo Usuario"
2. **Buscar:** Por número o nombre en la parte superior
3. **Editar:** Doble clic en usuario o seleccionar y editar
4. **Historial:** Botón "Ver Historial de Pagos"

### Módulo de Registro de Pagos
1. **Buscar Usuario:** Por número o nombre
2. **Seleccionar Año:** Usar flechas para cambiar año
3. **Seleccionar Meses:** Clic en meses a pagar (verde = pagado, azul = seleccionado)
4. **Conceptos Adicionales:** Agregar cooperaciones, multas, etc.
5. **Procesar Pago:** Revisar total y confirmar
6. **Generar Recibo:** Automático al procesar pago

### Módulo de Configuración
- **Configuración General:** Cuota mensual e información del comité
- **Conceptos de Cobro:** Gestionar conceptos adicionales
- **Seguridad:** Cambiar PIN y crear respaldos

## Respaldos de Seguridad

### Crear Respaldo
1. Ir a "Configuración del Sistema" > "Seguridad"
2. Clic en "Crear Respaldo"
3. Seleccionar ubicación y guardar

### Restaurar Respaldo
1. Ir a "Configuración del Sistema" > "Seguridad"
2. Clic en "Restaurar Respaldo"
3. Seleccionar archivo de respaldo
4. Confirmar restauración

**⚠️ IMPORTANTE:** Crear respaldos regulares para proteger la información.

## Solución de Problemas

### Error al iniciar
- Verificar que Python esté instalado correctamente
- Ejecutar `pip install -r requirements.txt` si existe
- Verificar permisos de escritura en la carpeta

### Error en la base de datos
- Verificar que el archivo `agua_potable.db` no esté corrupto
- Restaurar desde respaldo si es necesario
- Contactar soporte técnico

### Problemas con recibos PDF
- Verificar que reportlab esté instalado: `pip install reportlab`
- Comprobar permisos de escritura en carpeta `recibos/`

### Error de importación CSV
- Verificar formato del archivo CSV
- Comprobar codificación (preferir UTF-8)
- Revisar separadores (coma, punto y coma)

## Características Técnicas

- **Lenguaje:** Python 3.8+
- **Interface:** Tkinter (incluido en Python)
- **Base de datos:** SQLite3 (sin servidor)
- **PDF:** ReportLab
- **Imágenes:** Pillow (PIL)
- **Fechas:** python-dateutil

## Colaboración y Contribuciones

### Trabajar con GitHub
Si deseas contribuir al proyecto o tienes dudas sobre cómo funciona GitHub:
- **Lee la guía completa:** `GUIA_GITHUB.txt` - Explica Pull Requests, ramas, commits y más
- Incluye instrucciones paso a paso para colaboradores
- Responde preguntas frecuentes sobre Git y GitHub

### Flujo de Trabajo
1. Crea una rama para tus cambios
2. Haz commits con mensajes descriptivos
3. Sube tus cambios con `git push`
4. Crea un Pull Request en GitHub
5. Espera revisión y merge

## Licencia y Soporte

Este sistema ha sido desarrollado específicamente para comités de agua potable.

### Contacto
Para soporte técnico o consultas, contactar al desarrollador.

### Actualizaciones
- Verificar regularmente actualizaciones
- Mantener respaldos antes de actualizar
- Seguir instrucciones de migración si aplican

---

**© 2024 Sistema de Gestión de Agua Potable**
*Desarrollado con Python para la comunidad*
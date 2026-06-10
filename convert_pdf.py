import os
import glob
import markdown
import pdfkit

# Configuración de carpetas
CARPETA_MD = "reportes_md"
CARPETA_PDF = "reportes_pdf"

# Ruta exacta donde instalaste wkhtmltopdf en Windows
# Verifica que esta ruta coincida con la de tu computadora
RUTA_WKHTMLTOPDF = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"

# Crear carpeta de salida si no existe
if not os.path.exists(CARPETA_PDF):
    os.makedirs(CARPETA_PDF)

# Configurar pdfkit para que encuentre el ejecutable en Windows
configuracion = pdfkit.configuration(wkhtmltopdf=RUTA_WKHTMLTOPDF)

# Estilo CSS para que las tablas del reporte se vean profesionales en el PDF
ESTILO_CSS = """
<style>
    body { font-family: Arial, sans-serif; margin: 40px; color: #333; }
    h1, h2 { color: #2c3e50; }
    table { width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 12px; }
    th, td { border: 1px solid #dddddd; padding: 8px; text-align: left; }
    th { background-color: #f2f2f2; font-weight: bold; }
    hr { border: 0; border-top: 1px solid #eee; margin: 20px 0; }
</style>
"""

# Obtener todos los archivos .md
archivos_md = glob.glob(os.path.join(CARPETA_MD, "*.md"))
total_archivos = len(archivos_md)

print(f"Iniciando la conversión de {total_archivos} archivos a PDF...")

for indice, ruta_md in enumerate(archivos_md, 1):
    # Leer el contenido del Markdown
    with open(ruta_md, "r", encoding="utf-8") as f:
        texto_md = f.read()

    # Convertir Markdown a HTML (habilitando la extensión de tablas)
    html_crudo = markdown.markdown(texto_md, extensions=['tables'])

    # Armar el HTML final con el estilo CSS
    html_final = f"<html><head><meta charset='utf-8'>{ESTILO_CSS}</head><body>{html_crudo}</body></html>"

    # Definir el nombre del archivo de salida
    nombre_base = os.path.basename(ruta_md)
    nombre_pdf = nombre_base.replace(".md", ".pdf")
    ruta_pdf = os.path.join(CARPETA_PDF, nombre_pdf)

    # Configurar opciones del PDF (tamaño carta, márgenes, etc.)
    opciones = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'enable-local-file-access': None  # Permite cargar imágenes o estilos locales si los hubiera
    }

    # Generar el PDF
    try:
        pdfkit.from_string(html_final, ruta_pdf, configuration=configuracion, options=opciones)
        print(f"[{indice}/{total_archivos}] Creado: {nombre_pdf}")
    except Exception as e:
        print(f"Error al convertir {nombre_base}: {e}")

print("\n¡Conversión masiva completada! Revisa la carpeta 'reportes_pdf'.")
import os
import random
import shutil
from datetime import datetime, timedelta

# Configuración inicial
NUM_REPORTES = 1000  # Generará tus 50 reportes independientes
CARPETA_SALIDA = "reportes_md"
NOMBRE_ZIP = "reportes_aguajales"

# Crear o limpiar el directorio
if os.path.exists(CARPETA_SALIDA):
    shutil.rmtree(CARPETA_SALIDA)
os.makedirs(CARPETA_SALIDA)

fecha_base = datetime(2026, 6, 9)


def generar_tabla_imagenes(fecha_str, lat_base, lon_base, num_imagenes):
    tabla = "| ID | Archivo | Usar | Estado | Cobertura | Área | Árboles | GPS |\n"
    tabla += "|---|---|---|---|---|---|---|---|\n"

    fallos_totales = 0

    for i in range(num_imagenes):
        # Simular fallos aleatorios (aprox 10% de probabilidad)
        fallo = random.random() < 0.10
        estado = "Fallo" if fallo else "OK"
        usar = "Sí"

        # Calcular grilla GPS (adaptable a la cantidad de imágenes)
        fila = i // 10
        columna = i % 10
        lat = lat_base + (fila * 0.000200)
        lon = lon_base + (columna * 0.000200)

        if fallo:
            cobertura, area, arboles = "-", "-", "-"
            fallos_totales += 1
        else:
            cobertura = f"{random.uniform(5.0, 55.0):.2f} %"
            area = f"{random.uniform(100.0, 1200.0):.2f} m²"
            arboles = str(random.randint(1, 28))

        # Mantengo la fecha en el nombre de la foto de la tabla (formato DJI) para darle realismo
        archivo = f"DJI_{fecha_str.replace('-', '')}_{str(i + 1).zfill(3)}_V.JPG"

        tabla += f"| {i} | {archivo} | {usar} | {estado} | {cobertura} | {area} | {arboles} | {lat:.6f}, {lon:.6f} |\n"

    return tabla, fallos_totales


# Generar los archivos Markdown
for r in range(1, NUM_REPORTES + 1):
    fecha_reporte = fecha_base + timedelta(days=r)
    fecha_str = fecha_reporte.strftime("%Y-%m-%d")

    # Seleccionar aleatoriamente la cantidad de imágenes para este reporte específico
    num_imagenes = random.choice([140, 160, 180, 200])

    # Variar ligeramente el punto de inicio GPS por zona
    lat_inicio = -4.611000 + (r * 0.001000)
    lon_inicio = -74.491000 - (r * 0.001000)

    # Generar tabla y obtener conteo de fallos reales
    tabla_markdown, fallos_reales = generar_tabla_imagenes(fecha_str, lat_inicio, lon_inicio, num_imagenes)

    procesadas_ok = num_imagenes - fallos_reales

    contenido_md = f"""# Reporte de resultados - Aguajales (Zona {r})

**Generado:** {fecha_str}

---

## 1. Resumen de procesamiento

| Campo | Valor |
|---|---|
| Total de imágenes | {num_imagenes} |
| Imágenes seleccionadas | {num_imagenes} |
| Imágenes procesadas correctamente | {procesadas_ok} |
| Imágenes con fallos | {fallos_reales} |
| Imágenes pendientes | 0 |
| Seleccionadas y procesadas | {procesadas_ok} |

---

## 2. Resultados globales

| Campo | Valor |
|---|---|
| Cobertura media de imágenes seleccionadas | {random.uniform(20.0, 30.0):.2f} % |
| Cobertura global aproximada por heatmap | {random.uniform(15.0, 25.0):.2f} % |
| Área acumulada de aguajal | {random.uniform(40000.0, 80000.0):.2f} m² |
| Área de aguajal estimada por heatmap | {random.uniform(10000.0, 25000.0):.2f} m² |
| Área cubierta por heatmap | {random.uniform(60000.0, 100000.0):.2f} m² |
| Árboles de aguaje estimados | {procesadas_ok * random.randint(10, 18)} |
| Imágenes usadas en heatmap | {procesadas_ok} |

---

## 3. Parámetros usados

| Parámetro | Valor |
|---|---|
| Dispositivo | GPU NVIDIA / CUDA |
| Modo de procesamiento | Ultrarrápido |
| GSD | 1,0100 cm/px |
| Área por árbol de aguaje | 30,00 m² |
| Altura del objeto | 30,00 m |

---

## 4. Detalle por imagen

{tabla_markdown}
"""

    # Crear el nombre del archivo con enumeración (01, 02, ..., 50) sin la fecha
    nombre_archivo = f"reporte_aguajales_{str(r).zfill(2)}.md"
    ruta_archivo = os.path.join(CARPETA_SALIDA, nombre_archivo)

    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(contenido_md)

# Crear el archivo .zip
shutil.make_archive(NOMBRE_ZIP, 'zip', CARPETA_SALIDA)

print(f"¡Éxito! Se han generado {NUM_REPORTES} reportes estructurados en la carpeta '{CARPETA_SALIDA}'.")
print(f"También se ha creado el archivo comprimido: {NOMBRE_ZIP}.zip")

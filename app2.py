import openpyxl
import streamlit as st

# Cargar el archivo Excel actualizado
workbook = openpyxl.load_workbook("Analisis_acciones_actualizado.xlsx")
sheet = workbook.active

# Leer los valores de las celdas
valores = [sheet[f'B{i}'].value for i in range(2, 18)]
puntuacion = sheet['B18'].value

# Nombres de los indicadores correspondientes a cada celda
indicadores = [
    "Nombre corto", "Símbolo", "P/E trailing", "P/E forward",
    "Margen de beneficio", "Relación empresa/EBITDA", "Porcentaje de insiders",
    "Efectivo total", "Deuda total", "EBITDA", "Crecimiento de ganancias trimestrales",
    "Beta", "Rendimiento del dividendo", "Precio actual", "Precio objetivo promedio", 
    "Última fecha de actualización"
]

# Mostrar los valores con etiquetas
for indicador, valor in zip(indicadores, valores):
    st.write(f"{indicador}: {valor}")

# Mostrar la puntuación de la acción
if puntuacion is not None:
    st.write(f"Puntuación de la acción (de B18): {puntuacion}")
else:
    st.write("No hay puntuación disponible en B18.")

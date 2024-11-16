import openpyxl
import streamlit as st

# Cargar el archivo Excel actualizado
workbook = openpyxl.load_workbook("Analisis_acciones_actualizado.xlsx")
sheet = workbook.active

# Leer los valores de las celdas B2 a B17
valores = [sheet[f'B{i}'].value for i in range(2, 18)]

# Mostrar los valores con Streamlit
st.write("Valores de las celdas B2 a B17:")
for i, valor in enumerate(valores, start=2):
    st.write(f"B{i}: {valor}")

# Leer la puntuación de la celda B18
puntuacion = sheet['B18'].value
st.write(f"Puntuación de la acción (B18): {puntuacion}")

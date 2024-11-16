import openpyxl
import streamlit as st

# Cargar el archivo Excel actualizado
workbook = openpyxl.load_workbook("Analisis_acciones_actualizado.xlsx")
sheet = workbook.active

# Leer el valor numérico de la celda B2
valor_b2 = sheet['B2'].value

# Mostrar el valor en la interfaz de Streamlit
st.write(f"El valor de la celda B2 es: {valor_b2}")

import openpyxl
import streamlit as st

# Cargar el archivo Excel actualizado
workbook = openpyxl.load_workbook("Analisis_acciones_actualizado.xlsx")
sheet = workbook.active

# Leer el valor de la celda AY60
valor_AY60 = sheet['AY60'].value

# Mostrar el valor de la celda en la interfaz
if valor_AY60 is not None:
    st.write(f"El valor de la celda AY60 es: {valor_AY60}")
else:
    st.write("La celda AY60 está vacía.")

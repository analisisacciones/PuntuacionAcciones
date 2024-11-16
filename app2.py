import openpyxl
import streamlit as st

# Cargar el archivo Excel actualizado
workbook = openpyxl.load_workbook("Analisis_acciones_actualizado.xlsx")
sheet = workbook.active

# Leer el valor numérico de la celda AY60
valor_ay60 = sheet['AY60'].value

# Verificar si la celda no está vacía y mostrar el valor
if valor_ay60 is not None:
    st.write("El valor de la celda AY60 es:", valor_ay60)
else:
    st.write("La celda AY60 está vacía.")

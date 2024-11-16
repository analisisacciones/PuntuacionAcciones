import xlwings as xw
import streamlit as st

# Abrir el archivo Excel con xlwings
wb = xw.Book('Analisis_acciones_actualizado.xlsx')
sheet = wb.sheets[0]

# Obtener el valor de la celda AY60
valor_ay60 = sheet.range('AY60').value

# Mostrar el valor en la interfaz de Streamlit
st.write(f"El valor de la celda AY60 es: {valor_ay60}")

import openpyxl
import requests
import yfinance as yf
import streamlit as st

# Cargar el archivo de Excel desde GitHub
excel_url = "https://raw.githubusercontent.com/analisisacciones/PuntuacionAcciones/main/Analisis_acciones.xlsx"
response = requests.get(excel_url)

# Guardar el archivo temporalmente
with open("Analisis_acciones.xlsx", "wb") as file:
    file.write(response.content)

# Cargar el archivo de Excel con openpyxl
workbook = openpyxl.load_workbook("Analisis_acciones.xlsx")
sheet = workbook.active

# Función para obtener y dar formato a los datos financieros
def obtener_datos(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.info

    datos = [
        data.get('shortName', 'N/A'),
        data.get('symbol', 'N/A'),
        round(data.get('trailingPE', 'N/A'), 2) if data.get('trailingPE') else "N/A",
        round(data.get('forwardPE', 'N/A'), 2) if data.get('forwardPE') else "N/A",
        round(data.get('profitMargins', 'N/A') * 100, 2) if data.get('profitMargins') else "N/A",
        round(data.get('enterpriseToEbitda', 'N/A'), 2) if data.get('enterpriseToEbitda') else "N/A",
        round(data.get('heldPercentInsiders', 'N/A') * 100, 2) if data.get('heldPercentInsiders') else "N/A",
        round(data.get('totalCash', 'N/A'), 2) if data.get('totalCash') else "N/A",
        round(data.get('totalDebt', 'N/A'), 2) if data.get('totalDebt') else "N/A",
        round(data.get('ebitda', 'N/A'), 2) if data.get('ebitda') else "N/A",
        round(data.get('earningsQuarterlyGrowth', 'N/A') * 100, 2) if data.get('earningsQuarterlyGrowth') else "N/A",
        round(data.get('beta', 'N/A'), 2) if data.get('beta') else "N/A",
        round(data.get('dividendYield', 'N/A') * 100, 2) if data.get('dividendYield') else "N/A",
        round(data.get('currentPrice', 'N/A'), 2) if data.get('currentPrice') else "N/A",
        round(data.get('targetMeanPrice', 'N/A'), 2) if data.get('targetMeanPrice') else "N/A",
        ticker.history(period="1d").index[-1].strftime('%Y-%m-%d') if not ticker.history(period="1d").empty else "N/A"
    ]
    
    return datos

# Interfaz en Streamlit
def main():
    st.title("Análisis de Acciones")
    ticker_symbol = st.text_input("Introduce el símbolo de la acción (por ejemplo, TSLA para Tesla):")

    if ticker_symbol:
        # Obtener los datos
        datos = obtener_datos(ticker_symbol)

        # Actualizar las celdas correspondientes del Excel con los datos
        sheet['B2'] = datos[0]
        sheet['B3'] = datos[1]
        sheet['B4'] = datos[2]
        sheet['B5'] = datos[3]
        sheet['B6'] = datos[4]
        sheet['B7'] = datos[5]
        sheet['B8'] = datos[6]
        sheet['B9'] = datos[7]
        sheet['B10'] = datos[8]
        sheet['B11'] = datos[9]
        sheet['B12'] = datos[10]
        sheet['B13'] = datos[11]
        sheet['B14'] = datos[12]
        sheet['B15'] = datos[13]
        sheet['B16'] = datos[14]
        sheet['B17'] = datos[15]

        # Guardar el archivo con los cambios
        workbook.save("Analisis_acciones_actualizado.xlsx")

        # Leer los valores de las celdas de B2 a B17
        valores = [sheet[f'B{i}'].value for i in range(2, 18)]

        # Nombres de los indicadores correspondientes a cada celda
        indicadores = [
            "Nombre corto", "Símbolo", "P/E trailing", "P/E forward",
            "Margen de beneficio (%)", "Relación empresa/EBITDA",
            "Porcentaje de insiders (%)", "Efectivo total",
            "Deuda total", "EBITDA", "Crecimiento de ganancias trimestrales (%)",
            "Beta", "Rendimiento del dividendo (%)", "Precio actual",
            "Precio objetivo promedio", "Última fecha de actualización"
        ]

        # Mostrar los valores con etiquetas
        for indicador, valor in zip(indicadores, valores):
            st.write(f"{indicador}: {valor}")

if __name__ == "__main__":
    main()

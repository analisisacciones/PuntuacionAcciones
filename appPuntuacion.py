import xlwings as xw
import yfinance as yf
import streamlit as st

# Función para obtener y dar formato a los datos financieros
def obtener_datos(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.info

    # Extrae los datos de interés y los devuelve como una lista de valores
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
        round(data.get('earningsQuarterlyGrowth', 'N/A'), 2) if data.get('earningsQuarterlyGrowth') else "N/A",
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

        # Abrir el archivo con xlwings (y no con openpyxl)
        with xw.App(visible=False) as app:
            wb = app.books.open("Analisis_acciones.xlsx")
            sheet = wb.sheets[0]
            
            # Actualizar las celdas correspondientes del Excel
            sheet.range('B2').value = datos[0]
            sheet.range('B3').value = datos[1]
            sheet.range('B4').value = datos[2]
            sheet.range('B5').value = datos[3]
            sheet.range('B6').value = datos[4]
            sheet.range('B7').value = datos[5]
            sheet.range('B8').value = datos[6]
            sheet.range('B9').value = datos[7]
            sheet.range('B10').value = datos[8]
            sheet.range('B11').value = datos[9]
            sheet.range('B12').value = datos[10]
            sheet.range('B13').value = datos[11]
            sheet.range('B14').value = datos[12]
            sheet.range('B15').value = datos[13]
            sheet.range('B16').value = datos[14]

            # Obtener el valor calculado de la fórmula en B18
            puntaje_compra = sheet.range('B18').value
            st.write(f"Puntuación de compra de la empresa: {puntaje_compra}")
            
            # Guardar el archivo con los cambios
            wb.save()

if __name__ == "__main__":
    main()

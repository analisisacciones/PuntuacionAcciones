import yfinance as yf
import streamlit as st

# Función para obtener y dar formato a los datos financieros
def obtener_datos(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.info

    # Asegurarse de que si un valor no existe, se devuelva 'N/A'
    datos = [
        data.get('shortName', 'N/A'),
        data.get('symbol', 'N/A'),
        round(data.get('trailingPE', 'N/A'), 2) if data.get('trailingPE') is not None else "N/A",
        round(data.get('forwardPE', 'N/A'), 2) if data.get('forwardPE') is not None else "N/A",
        f"{round(data.get('profitMargins', 'N/A') * 100, 2)}%" if data.get('profitMargins') is not None else "N/A",
        round(data.get('enterpriseToEbitda', 'N/A'), 2) if data.get('enterpriseToEbitda') is not None else "N/A",
        f"{round(data.get('heldPercentInsiders', 'N/A') * 100, 2)}%" if data.get('heldPercentInsiders') is not None else "N/A",
        round(data.get('totalCash', 'N/A'), 2) if data.get('totalCash') is not None else "N/A",
        round(data.get('totalDebt', 'N/A'), 2) if data.get('totalDebt') is not None else "N/A",
        round(data.get('ebitda', 'N/A'), 2) if data.get('ebitda') is not None else "N/A",
        f"{round(data.get('earningsQuarterlyGrowth', 'N/A') * 100, 2)}%" if data.get('earningsQuarterlyGrowth') is not None else "N/A",
        round(data.get('beta', 'N/A'), 2) if data.get('beta') is not None else "N/A",
        f"{round(data.get('dividendYield', 0) * 100, 2)}%" if data.get('dividendYield', 0) is not None else "N/A",  # Cambio aquí
        round(data.get('currentPrice', 'N/A'), 2) if data.get('currentPrice') is not None else "N/A",
        round(data.get('targetMeanPrice', 'N/A'), 2) if data.get('targetMeanPrice') is not None else "N/A",
        ticker.history(period="1d").index[-1].strftime('%Y-%m-%d') if not ticker.history(period="1d").empty else "N/A"
    ]
    
    return datos

# Interfaz en Streamlit
def main():
    st.title("Análisis de Acciones")
    ticker_symbol = st.text_input("Introduce el símbolo de la acción (por ejemplo, TSLA para Tesla):")

    if ticker_symbol:
        try:
            # Obtener los datos
            datos = obtener_datos(ticker_symbol)

            # Verificar que los datos no sean vacíos
            if not any(dato == 'N/A' for dato in datos):
                # Nombres de los indicadores correspondientes
                indicadores = [
                    "Nombre corto", "Símbolo", "P/E trailing", "P/E forward",
                    "Margen de beneficio", "Relación empresa/EBITDA",
                    "Porcentaje de insiders", "Efectivo total",
                    "Deuda total", "EBITDA", "Crecimiento de ganancias trimestrales",
                    "Beta", "Rendimiento del dividendo", "Precio actual",
                    "Precio objetivo promedio", "Última fecha de actualización"
                ]

                # Mostrar los datos con etiquetas
                for indicador, valor in zip(indicadores, datos):
                    st.write(f"{indicador}: {valor}")

            else:
                st.error("Los datos obtenidos contienen valores no válidos.")
        except Exception as e:
            st.error(f"Error al obtener los datos: {e}")

if __name__ == "__main__":
    main()

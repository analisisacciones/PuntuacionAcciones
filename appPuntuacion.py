ues esos datos se sacan de este codigo que saca los datos de yfinance, mira te paso el codigo que saca los datos de yfinance, integrame los dos codigos en uno para que funcione. codigo:                                                                                                                                                                                import yfinance as yf
import streamlit as st

# Función para obtener y formatear los datos financieros
def obtener_datos(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.info
    
    datos = {
        "Nombre corto": data.get('shortName', 'N/A'),
        "Símbolo": data.get('symbol', 'N/A'),
        "P/E trailing": round(data.get('trailingPE', 'N/A'), 2) if data.get('trailingPE') else "N/A",
        "P/E forward": round(data.get('forwardPE', 'N/A'), 2) if data.get('forwardPE') else "N/A",
        "Margen de beneficio": f"{round(data.get('profitMargins', 'N/A') * 100, 2)}%" if data.get('profitMargins') else "N/A",
        "Relación empresa/EBITDA": round(data.get('enterpriseToEbitda', 'N/A'), 2) if data.get('enterpriseToEbitda') else "N/A",
        "Porcentaje de insiders": f"{round(data.get('heldPercentInsiders', 'N/A') * 100, 2)}%" if data.get('heldPercentInsiders') else "N/A",
        "Efectivo total": round(data.get('totalCash', 'N/A'), 2) if data.get('totalCash') else "N/A",
        "Deuda total": round(data.get('totalDebt', 'N/A'), 2) if data.get('totalDebt') else "N/A",
        "EBITDA": round(data.get('ebitda', 'N/A'), 2) if data.get('ebitda') else "N/A",
        "Crecimiento de ganancias trimestrales": f"{round(data.get('earningsQuarterlyGrowth', 'N/A') * 100, 2)}%" if data.get('earningsQuarterlyGrowth') else "N/A",
        "Beta": round(data.get('beta', 'N/A'), 2) if data.get('beta') else "N/A",
        "Rendimiento del dividendo": f"{round(data.get('dividendYield', 'N/A') * 100, 2)}%" if data.get('dividendYield') else "N/A",
        "Precio actual": round(data.get('currentPrice', 'N/A'), 2) if data.get('currentPrice') else "N/A",
        "Precio objetivo promedio": round(data.get('targetMeanPrice', 'N/A'), 2) if data.get('targetMeanPrice') else "N/A",
        "Última fecha de actualización": ticker.history(period="1d").index[-1].strftime('%Y-%m-%d') if not ticker.history(period="1d").empty else "N/A"
    }
    
    return datos

# Interfaz en Streamlit
def main():
    st.title("Análisis de Acciones")
    ticker_symbol = st.text_input("Introduce el símbolo de la acción (por ejemplo, TSLA para Tesla):")

    if ticker_symbol:
        try:
            # Obtener los datos
            datos = obtener_datos(ticker_symbol)

            # Mostrar los datos
            for key, value in datos.items():
                st.write(f"{key}: {value}")

        except Exception as e:
            st.error(f"Error al obtener los datos: {e}")

if __name__ == "__main__":
    main()

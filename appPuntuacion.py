import yfinance as yf
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

# Funciones para calcular las puntuaciones
def calcular_pe_trailing(pe_trailing):
    if pe_trailing < 16:
        return 100
    elif pe_trailing <= 22.5:
        return 60
    else:
        return 30

def calcular_analisis_pe_forward(pe_forward, pe_trailing):
    diferencia = pe_forward - pe_trailing
    if diferencia > 0:
        return 0
    elif 0 >= diferencia > -2:
        return 30
    else:
        return 100

def calcular_pe_forward(pe_forward):
    if pe_forward < 16:
        return 100
    elif pe_forward <= 22.5:
        return 60
    else:
        return 30

def calcular_margen_beneficio(margen_beneficio):
    if margen_beneficio <= 0.05:
        return 15
    elif margen_beneficio <= 0.1:
        return 40
    elif margen_beneficio <= 0.2:
        return 75
    else:
        return 100

def calcular_relacion_empresa_ebitda(relacion_ebitda):
    if relacion_ebitda <= 10:
        return 100
    elif relacion_ebitda <= 15:
        return 70
    else:
        return 30

def porcentaje_insiders(valor):
    if valor <= 0.05:
        return 15
    elif valor <= 0.1:
        return 40
    elif valor <= 0.2:
        return 75
    else:
        return 100

def calcular_crecimiento_ganancias(crecimiento_ganancias):
    if crecimiento_ganancias <= 0.05:
        return 15
    elif crecimiento_ganancias <= 0.15:
        return 60
    elif crecimiento_ganancias <= 0.25:
        return 90
    else:
        return 100

def calcular_beta(beta):
    if 0.8 <= beta <= 1.2:
        return 100
    elif 0 < beta <= 0.3:
        return 20
    elif 0.3 < beta < 0.8:
        return 70
    elif 1.2 <= beta < 1.6:
        return 60
    elif 1.6 <= beta < 2:
        return 40
    elif beta > 2:
        return 20
    else:
        return 0

def calcular_dividendos(dividendos):
    if dividendos == "N/A":
        return 0
    elif 0 < dividendos <= 0.02:
        return 75
    elif dividendos > 0.02:
        return 100
    else:
        return 0

def calcular_cash_deuda(cash, deuda):
    if deuda == 0:
        return None
    
    ratio = (cash - deuda) / deuda

    if 0 <= ratio <= 1:
        return 80
    elif ratio > 1:
        return 100
    elif -0.5 < ratio < 0:
        return 50
    elif ratio < -0.5:
        return 10
    else:
        return None

def calcular_deuda_ebitda(deuda, ebitda):
    if ebitda == 0:
        return None
    
    ratio = deuda / ebitda

    if 0 <= ratio <= 2.5:
        return 100
    elif 2.5 < ratio <= 4:
        return 60
    elif 4 < ratio <= 10:
        return 10
    elif ratio > 10:
        return 0
    else:
        return None

def calcular_precio_esperado(precio_actual, precio_esperado):
    diferencia = (precio_esperado - precio_actual) / precio_actual
    if diferencia < 0:
        return 0
    elif 0 <= diferencia < 0.1:
        return 30
    elif 0.1 <= diferencia < 0.2:
        return 60
    elif 0.2 <= diferencia < 0.4:
        return 80
    else:
        return 100

# Función para calcular la puntuación final ponderada
def calcular_puntuacion_final(puntuaciones):
    pesos = [8.33, 13.89, 4.17, 12.50, 9.72, 9.72, 9.72, 2.78, 1.39, 9.72, 4.17, 13.89]
    puntuacion_final = 0
    for i in range(len(puntuaciones)):
        puntuacion_final += puntuaciones[i] * (pesos[i] / 100)
    return puntuacion_final

# Interfaz en Streamlit
def main():
    st.title("Análisis de Acciones")
    ticker_symbol = st.text_input("Introduce el símbolo de la acción (por ejemplo, TSLA para Tesla):")

    if ticker_symbol:
        try:
            # Obtener los datos
            datos = obtener_datos(ticker_symbol)

            # Extraer y calcular las puntuaciones
            pe_trailing = datos["P/E trailing"]
            pe_forward = datos["P/E forward"]
            margen_beneficio = datos["Margen de beneficio"]
            relacion_ebitda = datos["Relación empresa/EBITDA"]
            porcentaje_insiders_valor = datos["Porcentaje de insiders"]
            crecimiento_ganancias = datos["Crecimiento de ganancias trimestrales"]
            beta = datos["Beta"]
            dividendos = datos["Rendimiento del dividendo"]
            efectivo_total = datos["Efectivo total"]
            deuda_total = datos["Deuda total"]
            ebitda = datos["EBITDA"]
            precio_actual = datos["Precio actual"]
            precio_objetivo_promedio = datos["Precio objetivo promedio"]
            
            # Ponderar las puntuaciones
            puntuaciones = [
                calcular_pe_trailing(pe_trailing),
                calcular_analisis_pe_forward(pe_forward, pe_trailing),
                calcular_pe_forward(pe_forward),
                calcular_margen_beneficio(margen_beneficio),
                calcular_relacion_empresa_ebitda(relacion_ebitda),
                porcentaje_insiders(porcentaje_insiders_valor),
                calcular_crecimiento_ganancias(crecimiento_ganancias),
                calcular_beta(beta),
                calcular_dividendos(dividendos),
                calcular_cash_deuda(efectivo_total, deuda_total),
                calcular_deuda_ebitda(deudaHe integrado el código de `yfinance` y el cálculo de las puntuaciones en un solo flujo. Aquí tienes el código completo y optimizado:

```python
import yfinance as yf
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

# Funciones para calcular las puntuaciones
def calcular_pe_trailing(pe_trailing):
    if pe_trailing < 16:
        return 100
    elif pe_trailing <= 22.5:
        return 60
    else:
        return 30

def calcular_analisis_pe_forward(pe_forward, pe_trailing):
    diferencia = pe_forward - pe_trailing
    if diferencia > 0:
        return 0
    elif 0 >= diferencia > -2:
        return 30
    else:
        return 100

def calcular_pe_forward(pe_forward):
    if pe_forward < 16:
        return 100
    elif pe_forward <= 22.5:
        return 60
    else:
        return 30

def calcular_margen_beneficio(margen_beneficio):
    if margen_beneficio <= 0.05:
        return 15
    elif margen_beneficio <= 0.1:
        return 40
    elif margen_beneficio <= 0.2:
        return 75
    else:
        return 100

def calcular_relacion_empresa_ebitda(relacion_ebitda):
    if relacion_ebitda <= 10:
        return 100
    elif relacion_ebitda <= 15:
        return 70
    else:
        return 30

def porcentaje_insiders(valor):
    if valor <= 0.05:
        return 15
    elif valor <= 0.1:
        return 40
    elif valor <= 0.2:
        return 75
    else:
        return 100

def calcular_crecimiento_ganancias(crecimiento_ganancias):
    if crecimiento_ganancias <= 0.05:
        return 15
    elif crecimiento_ganancias <= 0.15:
        return 60
    elif crecimiento_ganancias <= 0.25:
        return 90
    else:
        return 100

def calcular_beta(beta):
    if 0.8 <= beta <= 1.2:
        return 100
    elif 0 < beta <= 0.3:
        return 20
    elif 0.3 < beta < 0.8:
        return 70
    elif 1.2 <= beta < 1.6:
        return 60
    elif 1.6 <= beta < 2:
        return 40
    elif beta > 2:
        return 20
    else:
        return 0

def calcular_dividendos(dividendos):
    if dividendos == "N/A":
        return 0
    elif 0 < dividendos <= 0.02:
        return 75
    elif dividendos > 0.02:
        return 100
    else:
        return 0

def calcular_cash_deuda(cash, deuda):
    if deuda == 0:
        return None
    
    ratio = (cash - deuda) / deuda

    if 0 <= ratio <= 1:
        return 80
    elif ratio > 1:
        return 100
    elif -0.5 < ratio < 0:
        return 50
    elif ratio < -0.5:
        return 10
    else:
        return None

def calcular_deuda_ebitda(deuda, ebitda):
    if ebitda == 0:
        return None
    
    ratio = deuda / ebitda

    if 0 <= ratio <= 2.5:
        return 100
    elif 2.5 < ratio <= 4:
        return 60
    elif 4 < ratio <= 10:
        return 10
    elif ratio > 10:
        return 0
    else:
        return None

def calcular_precio_esperado(precio_actual, precio_esperado):
    diferencia = (precio_esperado - precio_actual) / precio_actual
    if diferencia < 0:
        return 0
    elif 0 <= diferencia < 0.1:
        return 30
    elif 0.1 <= diferencia < 0.2:
        return 60
    elif 0.2 <= diferencia < 0.4:
        return 80
    else:
        return 100

# Función para calcular la puntuación final ponderada
def calcular_puntuacion_final(puntuaciones):
    pesos = [8.33, 13.89, 4.17, 12.50, 9.72, 9.72, 9.72, 2.78, 1.39, 9.72, 4.17, 13.89]
    puntuacion_final = 0
    for i in range(len(puntuaciones)):
        puntuacion_final += puntuaciones[i] * (pesos[i] / 100)
    return puntuacion_final

# Interfaz en Streamlit
def main():
    st.title("Análisis de Acciones")
    ticker_symbol = st.text_input("Introduce el símbolo de la acción (por ejemplo, TSLA para Tesla):")

    if ticker_symbol:
        try:
            # Obtener los datos
            datos = obtener_datos(ticker_symbol)

            # Extraer y calcular las puntuaciones
            pe_trailing = datos["P/E trailing"]
            pe_forward = datos["P/E forward"]
            margen_beneficio = datos["Margen de beneficio"]
            relacion_ebitda = datos["Relación empresa/EBITDA"]
            porcentaje_insiders_valor = datos["Porcentaje de insiders"]
            crecimiento_ganancias = datos["Crecimiento de ganancias trimestrales"]
            beta = datos["Beta"]
            dividendos = datos["Rendimiento del dividendo"]
            efectivo_total = datos["Efectivo total"]
            deuda_total = datos["Deuda total"]
            ebitda = datos["EBITDA"]
            precio_actual = datos["Precio actual"]
            precio_objetivo_promedio = datos["Precio objetivo promedio"]
            
           # Ponderar las puntuaciones
puntuaciones = [
    calcular_pe_trailing(pe_trailing),
    calcular_analisis_pe_forward(pe_forward, pe_trailing),
    calcular_pe_forward(pe_forward),
    calcular_margen_beneficio(margen_beneficio),
    calcular_relacion_empresa_ebitda(relacion_ebitda),
    porcentaje_insiders(porcentaje_insiders_valor),
    calcular_crecimiento_ganancias(crecimiento_ganancias),
    calcular_beta(beta),
    calcular_dividendos(dividendos),
    calcular_cash_deuda(efectivo_total, deuda_total),
    calcular_deuda_ebitda(deuda_total, ebitda),
    calcular_precio_esperado(precio_actual, precio_objetivo_promedio)
]

            
            # Calcular la puntuación final ponderada
            puntuacion_final = calcular_puntuacion_final(puntuaciones)

            # Mostrar los datos y la puntuación final
            for key, value in datos.items():
                st.write(f"{key}: {value}")
                
            st.write(f"Puntuación final ponderada: {round(puntuacion_final, 2)}")
        
        except Exception as e:
            st.error(f"Error al obtener los datos: {e}")

if __name__ == "__main__":
    main()

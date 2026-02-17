import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from model import OracleConnection
from consultas import query_por_fechas
import folium


def create_incidents_map(df):
    """Create a folium map with incident locations."""
    # Filter out rows with missing coordinates
    #Centra el mapa en las coordenadas 40.326366, -3.768147    
    df_map = df.dropna(subset=['coordX', 'coordY'])
    
    if df_map.empty:
        return None
    
    # Create map centered on the mean coordinates
    center_lat = df_map['coordY'].mean()
    center_lon = df_map['coordX'].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
    
    # Add markers for each incident
    for idx, row in df_map.iterrows():
        folium.Marker(
            location=[row['coordY'], row['coordX']],
            popup=f"{row['lugar']}<br>{row['hecho']}",
            tooltip=row['motivo']
        ).add_to(m)
    
    return m


def main():
    st.set_page_config(page_title="Stadísticas Streamlit", page_icon="📊")

    st.markdown("# Bienvenido a Stadísticas Streamlit! 📊")
    st.write("Conectando a la base de datos Oracle...")
    oracle_conn = OracleConnection()
    conn = oracle_conn.get_connection()

    if conn:
        print("Conexión exitosa a la base de datos Oracle!")
        st.success("¡Conexión exitosa a la base de datos Oracle!")
        # Aquí puedes agregar más lógica para interactuar con la base de datos
        
    else:
        st.error("No se pudo conectar a la base de datos Oracle.")

    st.header("Consulta por Fechas")

    fecha_inicio, hora_inicio ,fecha_fin , hora_fin = st.columns(4)
    with fecha_inicio:
        fecha_inicio = st.date_input("Fecha de Inicio", format="DD/MM/YYYY")
        fecha_inicio = fecha_inicio.strftime("%d/%m/%Y")
    with hora_inicio:
        hora_inicio = st.time_input("Hora de Inicio")
    with fecha_fin:
        fecha_fin = st.date_input("Fecha de Fin", format="DD/MM/YYYY")
        fecha_fin = fecha_fin.strftime("%d/%m/%Y")
    with hora_fin:
        hora_fin = st.time_input("Hora de Fin")

    

    query_fechas = query_por_fechas(fecha_inicio, fecha_fin, hora_inicio, hora_fin)

    result = oracle_conn.execute_query(conn, query_fechas)

   
    

    df = pd.DataFrame(result,columns=["numIncidencia", "anoIncidencia", "fechaAlta", "horaAlta", "hecho", "motivo","resultado", "lugar", "siglaVia", "via", "portal", "coordX", "coordY"])
    
     #Añade un filtro de selección múltiple para el motivo de finalización
    st.subheader("Filtrar por motivo de finalización")
    motivos = df['motivo'].unique().tolist()
    motivos_seleccionados = st.multiselect("Selecciona los motivos de finalización:", motivos, default=motivos)
    df = df[df['motivo'].isin(motivos_seleccionados)]

    #Crea un mapa de incidencias
    st.subheader("Mapa de incidencias")
    m = create_incidents_map(df)
    if m is None:
        st.info("No hay incidencias con coordenadas para mostrar en el mapa.")
    else:
        map_html = m._repr_html_()
        components.html(map_html, height=600)
    
    st.dataframe(df)

   
    st.divider()
    
    

    #Variable que almacena los motivos de finalización y su cantidad, ordenados y agrupados por año de incidencia
    actas_ano = df.groupby(['anoIncidencia', 'motivo']).size().reset_index(name='Cantidad')
    st.header("Cantidad de actas por año de incidencia y motivo de finalización:")
    st.write(actas_ano)


    #Tabla con fecha, hora y lugar de cada una de las incidencias con descripción que contiene el texto "vertido ilegal"
    df_vertido = df[df['hecho'].str.contains('VERTIDO ILEGAL', case=False, na=False)]
    st.header("Incidencias con descripción que contiene 'VERTIDO ILEGAL':")
    st.dataframe(df_vertido[['fechaAlta', 'horaAlta', 'lugar', 'hecho']])


    

    oracle_conn.close_connection(conn)

if __name__ == "__main__":
    main()
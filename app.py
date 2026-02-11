import streamlit as st
import pandas as pd
from model import OracleConnection
from consultas import query_por_fechas


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

    df = pd.DataFrame(result,columns=["numIncidencia", "anoIncidencia", "fechaAlta", "horaAlta", "descripcion", "hecho","motivoFinalizacion","resultadoAviso"])
    st.dataframe(df)

    
    col1, col2 = st.columns(2)

    with col1:
        actas = df['motivoFinalizacion'].value_counts().reset_index(name='Cantidad')
        st.write("Cantidad de actas por motivo de finalización:")   
        st.write(actas)
    with col2:
        actas = df['motivoFinalizacion'].value_counts().reset_index(name='Cantidad')
        st.write("Cantidad de actas por motivo de finalización:")   
        st.write(actas)

    #Variable que almacena los motivos de finalización y su cantidad, ordenados y agrupados por año de incidencia
    actas_ano = df.groupby(['anoIncidencia', 'motivoFinalizacion']).size().reset_index(name='Cantidad')
    st.write("Cantidad de actas por año de incidencia y motivo de finalización:")
    st.write(actas_ano)

    #Grafico de barrar de motivo de finalización por año de incidencia, pintando el valor en la barra
    st.write("Gráfico de barras de motivo de finalización por año de incidencia:")
    actas = df.groupby(['anoIncidencia', 'motivoFinalizacion']).size().reset_index(name='Cantidad')
    actas_pivot = actas.pivot(index='anoIncidencia', columns='motivoFinalizacion', values='Cantidad').fillna(0)
    st.bar_chart(actas_pivot)

    oracle_conn.close_connection(conn)

if __name__ == "__main__":
    main()
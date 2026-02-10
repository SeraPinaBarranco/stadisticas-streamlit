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
    fecha_inicio, fecha_fin = st.columns(2)
    with fecha_inicio:
        fecha_inicio = st.date_input("Fecha de Inicio")
    with fecha_fin:
        fecha_fin = st.date_input("Fecha de Fin")

    query_fechas = query_por_fechas()

    result = oracle_conn.execute_query(conn, query_fechas)

    df = pd.DataFrame(result,columns=["numIncidencia", "anoIncidencia", "fechaAlta", "horaAlta", "descripcion", "tipo", "nombre_denunciado", "apellidos1_denunciado", "apellidos2_denunciado", "doi_denunciado","via_denunciado","siglaVia_denunciado","siglas","nombre_calle","motivoFinalizacion","resultadoAviso"])
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

    

    oracle_conn.close_connection(conn)

if __name__ == "__main__":
    main()
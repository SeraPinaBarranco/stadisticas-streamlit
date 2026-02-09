import streamlit as st
from model import OracleConnection


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
        conn.close()
    else:
        st.error("No se pudo conectar a la base de datos Oracle.")

if __name__ == "__main__":
    main()
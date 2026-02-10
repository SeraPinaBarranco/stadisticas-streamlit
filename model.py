import oracledb
import streamlit as st

class OracleConnection:
    def __init__(self):
        # Acceder a los secretos definidos en el archivo TOML
        self.creds = st.secrets["oracle"]

    def get_connection(self):
        try:
            # Conexión en modo Thin usando los datos del TOML
            conn = oracledb.connect(
                user=self.creds["user"],
                password=self.creds["password"],
                host=self.creds["host"],
                port=self.creds["port"],
                service_name=self.creds["service_name"]
            )
            return conn
        except oracledb.Error as e:
            st.error(f"Error de conexión: {e}")
            return None
    
    def close_connection(self, conn):
        if conn:
            try:
                conn.close()
                st.success("Conexión cerrada exitosamente.")
            except oracledb.Error as e:
                st.error(f"Error al cerrar la conexión: {e}")

    def execute_query(self, conn, query):
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except oracledb.Error as e:
            st.error(f"Error al ejecutar la consulta: {e}")
            return None
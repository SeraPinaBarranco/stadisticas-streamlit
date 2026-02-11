from datetime import datetime
from ntpath import join
from turtle import left

from numpy import outer


def query_por_fechas_identificado(fecha_inicio=None, fecha_fin=None, hora_inicio=None, hora_fin=None, tabla=None, columna_fecha='fecha'):
    """
    Genera una consulta SQL filtrando por rango de fechas.
    
    Parameters:
    -----------
    fecha_inicio : datetime o str
        Fecha de inicio del rango (formato: YYYY-MM-DD o datetime object)
    fecha_fin : datetime o str
        Fecha final del rango (formato: YYYY-MM-DD o datetime object)
    hora_inicio : time o str
        Hora de inicio del rango (formato: HH:MM o time object)
    hora_fin : time o str
        Hora final del rango (formato: HH:MM o time object)
    tabla : str
        Nombre de la tabla a consultar
    columna_fecha : str
        Nombre de la columna de fecha a usar en el filtro (default: 'fecha')
    
    Returns:
    --------
    str
        Consulta SQL
    
    Example:
    --------
    >>> query = query_por_fechas('2025-01-01', '2025-12-31', 'ventas', 'fecha_venta')
    >>> print(query)
    """
    print(f"Generando consulta SQL para fechas: {fecha_inicio} - {fecha_fin} y horas: {hora_inicio} - {hora_fin}")
    if isinstance(fecha_inicio, datetime):
        fecha_inicio = fecha_inicio.strftime("%d/%m/%Y")
    
    if isinstance(fecha_fin, datetime):
        fecha_fin = fecha_fin.strftime("%d/%m/%Y")
    
    # query = f"""
    # SELECT * 
    # FROM {tabla}
    # WHERE {columna_fecha} >= TO_DATE('{fecha_inicio}', 'DD/MM/YYYY')
    # AND {columna_fecha} <= TO_DATE('{fecha_fin}', 'DD/MM/YYYY')
    # ORDER BY {columna_fecha}
    # """
    
    query=f"""
    select
        Incidencia.num_Incidencia as numIncidencia,
        Incidencia.ano_Incidencia as anoIncidencia,
        to_char(Incidencia.fechaAlta,
        'DD/MM/YYYY') as fechaAlta,
        to_char(Incidencia.fechaAlta,
        'HH24:MI') as horaAlta,
        hechoview2_.descripcion as descripcion,
        traduccion7_.texto as tipo,
        personavie10_.nombre as nombre_denunciado,
        personavie10_.apellidos1 as apellidos1_denunciado,
        personavie10_.apellidos2 as apellidos2_denunciado,
        personavie10_.doi as doi_denunciado,
        DBMS_LOB.SUBSTR( lugarview12_.descripcion, 8192, 1 ) as descripcion_denunciado,
        lugarview12_.via as via_denunciado,
        lugarview12_.siglaVia as siglaVia_denunciado,
        hechoview2_.descripcion as hecho,
        cbmotivofi13_.nombre as cbMotivoFinalizacion,
        cbresultad14_.nombre as cbResultadoAviso 
    
        from
            Incidencia Incidencia 
            left outer join
            Hecho hecho1_ 
            on Incidencia.hecho_id=hecho1_.id 
            left outer join
            HechoView hechoview2_ 
            on hecho1_.id=hechoview2_.id 
            left outer join
            Incidencia_R_Afectado incidencia3_ 
            on Incidencia.incidencia_id=incidencia3_.incidencia_id 
            left outer join
            Afectado afectado4_ 
            on incidencia3_.afectado_id=afectado4_.afectado_id 
            left outer join
            Tipo tipo5_ 
            on afectado4_.relacionafectado_id=tipo5_.tipo_id 
            left outer join
            Texto_Traducible textotradu6_ 
            on tipo5_.trNombre=textotradu6_.texto_traducible_id 
            left outer join
            Traduccion traduccion7_ 
            on textotradu6_.texto_traducible_id=traduccion7_.texto_traducible_id 
            and (
                traduccion7_.idioma_id=1
            ) 
            left outer join
        AfectadoPersona afectadope8_ 
            on afectado4_.afectado_id=afectadope8_.afectado_id 
        left outer join
        Persona persona9_ 
            on afectadope8_.persona_id=persona9_.persona_id 
        left outer join
        PersonaView personavie10_ 
            on persona9_.persona_id=personavie10_.persona_id 
        left outer join
        Lugar lugar11_ 
            on personavie10_.domicilioId=lugar11_.lugar_id 
        left outer join
        LugarView lugarview12_ 
            on lugar11_.lugar_id=lugarview12_.lugar_id 
        left outer join
        cbMotivoFinalizacion cbmotivofi13_ 
            on Incidencia.cbMotivoFinalizacion=cbmotivofi13_.id 
        left outer join
        cbResultadoAviso cbresultad14_ 
            on Incidencia.cbResultadoAviso=cbresultad14_.id 
        where
        (            
            upper(hechoview2_.descripcion) like '%21-VERTIDO ILEGAL%'
        )
        and Incidencia.fechaAlta>to_date('{fecha_inicio} {hora_inicio}', 'DD/MM/YYYY HH24:MI:SS') 
        and Incidencia.fechaAlta<=to_date('{fecha_fin} {hora_fin}', 'DD/MM/YYYY HH24:MI:SS')
        )
    """

    return query


def query_por_fechas(fecha_inicio=None, fecha_fin=None, hora_inicio=None, hora_fin=None, tabla=None, columna_fecha='fecha'):
    query = f"""                
        select
            Incidencia.num_Incidencia as numIncidencia,
            Incidencia.ano_Incidencia as anoIncidencia,
            to_char(Incidencia.fechaAlta,
            'DD/MM/YYYY') as fechaAlta,
            to_char(Incidencia.fechaAlta,
            'HH24:MI') as horaAlta,
            hechoview2_.descripcion as descripcion,
            hechoview2_.descripcion as hecho,
            cbmotivofi3_.nombre as cbMotivoFinalizacion,
            cbresultad4_.nombre as cbResultadoAviso 
            
            from
                Incidencia Incidencia 
            left outer join
                Hecho hecho1_ 
                    on Incidencia.hecho_id=hecho1_.id 
            left outer join
                HechoView hechoview2_ 
                    on hecho1_.id=hechoview2_.id 
            left outer join
                cbMotivoFinalizacion cbmotivofi3_ 
                    on Incidencia.cbMotivoFinalizacion=cbmotivofi3_.id 
            left outer join
                cbResultadoAviso cbresultad4_ 
                    on Incidencia.cbResultadoAviso=cbresultad4_.id 
                            where
                    (
                        
                        upper(hechoview2_.descripcion) like '%21-VERTIDO ILEGAL%' 
                        
                        and Incidencia.fechaAlta>to_date('{fecha_inicio} {hora_inicio}', 'DD/MM/YYYY HH24:MI:SS') 
                        and Incidencia.fechaAlta<=to_date('{fecha_fin} {hora_fin}', 'DD/MM/YYYY HH24:MI:SS')
                    )
            """
    return query
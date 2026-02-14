import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Divot Deals - Gestión de Golf", layout="wide", page_icon="⛳")

# --- ESTILOS CSS PERSONALIZADOS (AESTHETIC) ---
st.markdown("""
    <style>
    /* Importar fuente premium */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Fondo con gradiente inspirado en golf */
    .stApp {
        background: linear-gradient(135deg, #0f1a0f 0%, #1a3a14 100%);
        background-attachment: fixed;
    }
    
    /* Global Text Color */
    div[data-testid="stAppViewContainer"] p, 
    div[data-testid="stAppViewContainer"] span, 
    div[data-testid="stAppViewContainer"] label,
    div[data-testid="stAppViewContainer"] h1,
    div[data-testid="stAppViewContainer"] h2,
    div[data-testid="stAppViewContainer"] h3 {
        color: #ffffff !important;
    }

    /* Subtitles and secondary text */
    .stMarkdown div p {
        color: #e0e0e0 !important;
    }

    /* Titles with highlight */
    h1, h2, h3 {
        background: linear-gradient(to right, #ffffff, #a8e063);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
    }
    
    /* Contenedor de Login */
    .login-container {
        max-width: 450px;
        margin: 5% auto;
        padding: 3rem;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        text-align: center;
        color: #000000 !important;
    }
    
    .login-logo {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    .login-title {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0.2rem;
        background: linear-gradient(to right, #ffffff, #a8e063);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .login-subtitle {
        color: #a8e063 !important;
        -webkit-text-fill-color: #a8e063 !important;
        font-weight: 500;
        margin-bottom: 2rem;
        opacity: 0.9;
    }
    
    /* Estilo para inputs de Streamlit */
    div[data-baseweb="input"] input {
        color: #000000 !important;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #0f1a0f !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Tarjetas de Dashboard / Metrics */
    [data-testid="stMetricLabel"] {
        color: #e0e0e0 !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #a8e063 !important;
        font-weight: 700 !important;
        font-size: 2.2rem !important;
    }
    
    /* Tabs */
    button[data-baseweb="tab"] p {
        color: #e0e0e0 !important;
    }
    
    button[data-baseweb="tab"][aria-selected="true"] p {
        color: #a8e063 !important;
    }
    
    /* Botón de login custom */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #56ab2f 0%, #a8e063 100%);
        color: #000 !important;
        font-weight: 700;
        border-radius: 12px;
        border: none;
        padding: 0.75rem;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(168, 224, 99, 0.4);
    }
    
    /* Forzar fondo oscuro en Dataframes y Editores */
    .stDataFrame, [data-testid="stDataFrame"] {
        background-color: #000000 !important;
        border: 1px solid rgba(168, 224, 99, 0.3) !important;
        border-radius: 12px;
    }

    /* Estilo para tablas estáticas st.table */
    .stTable {
        background-color: #000000 !important;
        color: white !important;
    }
    
    .stTable thead tr th {
        background-color: #1a1a1a !important;
        color: #a8e063 !important;
    }

    /* Inputs y áreas de texto */
    div[data-baseweb="input"], div[data-baseweb="textarea"] {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(168, 224, 99, 0.4) !important;
    }
    
    /* Forzar color negro en etiquetas SOLO en el login para visibilidad */
    .login-container label {
        color: #000000 !important;
    }
    
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DE LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-logo">⛳</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-title">DIVOT DEALS</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-subtitle">Excellence in Golf Equipment</div>', unsafe_allow_html=True)
    
    with st.container():
        user = st.text_input("Usuario", placeholder="Tu usuario", key="login_user")
        pwd = st.text_input("Contraseña", type="password", placeholder="Tu contraseña", key="login_pwd")
        
        if st.button("INGRESAR AL SISTEMA"):
            if user == "Wilches1" and pwd == "Soygordo":
                st.session_state.logged_in = True
                st.success("Acceso concedido. ¡Bienvenido!")
                st.rerun()
            else:
                st.error("Credenciales incorrectas. Inténtalo de nuevo.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Si no está logueado, mostrar login y detener ejecución
if not st.session_state.logged_in:
    login()
    st.stop()

# --- BOTÓN DE CERRAR SESIÓN EN SIDEBAR ---
if st.sidebar.button("🚪 Cerrar Sesión"):
    st.session_state.logged_in = False
    st.rerun()

# --- CONEXIÓN Y CACHE ---
# --- CONEXIÓN Y CACHE ---
@st.cache_resource
def get_spreadsheet():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    import os
    json_path = "gestionnegocio.json"
    client = None
    if os.path.exists(json_path):
        try:
            client = gspread.service_account(filename=json_path)
        except Exception as e:
            st.error(f"Error JSON: {e}")
    elif "gcp_service_account" in st.secrets:
        try:
            creds_dict = dict(st.secrets["gcp_service_account"])
            if "private_key" in creds_dict:
                creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
            credentials = Credentials.from_service_account_info(creds_dict, scopes=scope)
            client = gspread.authorize(credentials)
        except Exception as e:
            st.error(f"Error Secrets: {e}")
    
    if client:
        return client.open_by_url(SHEET_URL)
    return None

@st.cache_data(ttl=300)
def get_sheet_df(sheet_name):
    """Lee una hoja y la devuelve como DataFrame, asegurando que tenga las columnas esperadas."""
    ss = get_spreadsheet()
    if not ss:
        return pd.DataFrame()
    
# --- ESTRUCTURA GLOBAL ---
STRUCTURE = {
    "Clientes": ["ID_Cliente", "Nombre_Razon_Social", "Dirección", "Teléfono", "Mail", "CUIT"],
    "Productos": ["ID_Producto", "Nombre", "Unidad", "Precio_Costo", "Precio_Venta"],
    "Pedidos": ["ID_Pedido", "ID_Cliente", "Fecha", "Estado", "Monto_Total", "Monto_Pagado", "Observaciones", "Materiales", "Obreros", "Fecha_Trabajo", "Fecha_Entrega", "Socio_Responsable", "Personal_Asignado"],
    "Pedidos_Detalle": ["ID_Detalle", "ID_Pedido", "ID_Producto", "Cantidad", "Precio_Historico"],
    "Tareas": ["ID_Tarea", "ID_Pedido", "Descripcion", "Fecha_Limite", "Estado"],
    "Gastos": ["ID_Gasto", "Fecha", "Categoria", "Descripcion", "Monto", "Socio"],
    "Socios": ["ID_Socio", "Nombre"],
    "Retiros_Socios": ["ID_Retiro", "ID_Socio", "Fecha", "Monto", "Concepto"]
}

@st.cache_data(ttl=300)
def get_sheet_df(sheet_name):
    """Lee una hoja y la devuelve como DataFrame, asegurando que tenga las columnas esperadas."""
    ss = get_spreadsheet()
    if not ss or sheet_name not in STRUCTURE:
        return pd.DataFrame()
    
    try:
        sh = ss.worksheet(sheet_name)
        data = sh.get_all_records()
        df = pd.DataFrame(data)
        
        expected_cols = STRUCTURE[sheet_name]
        if df.empty:
            return pd.DataFrame(columns=expected_cols)
        
        # Asegurar que todas las columnas esperadas existan
        for col in expected_cols:
            if col not in df.columns:
                df[col] = "" # Usar string vacío en lugar de None para evitar errores de tipo en pandas
                
        return df[expected_cols]
    except Exception as e:
        # Si falla get_all_records (ej: por headers duplicados o vacíos), intentamos con table
        try:
            sh = ss.worksheet(sheet_name)
            data = sh.get_all_values()
            if not data:
                return pd.DataFrame(columns=STRUCTURE.get(sheet_name, []))
            headers = data[0]
            df = pd.DataFrame(data[1:], columns=headers)
            expected_cols = STRUCTURE.get(sheet_name, [])
            for col in expected_cols:
                if col not in df.columns:
                    df[col] = ""
            return df[expected_cols]
        except Exception as e2:
            print(f"Error cargando {sheet_name}: {e2}")
            return pd.DataFrame()

SHEET_URL = "https://docs.google.com/spreadsheets/d/1gX16hMqj7xYPlDsNJeeNaQu8sz_2VR-SNDlZedm2vWM/edit"

# --- LÓGICA DE NAVEGACIÓN ---
st.sidebar.title("Navegación")
menu = st.sidebar.radio("Ir a:", ["Dashboard", "Clientes", "Productos", "Pedidos", "Logística/Pedidos", "Gastos", "Caja Socios"])

client = get_spreadsheet() # Esto ahora devuelve directamente el spreadsheet

if st.sidebar.button("🔄 Refrescar Datos"):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()

@st.cache_data(ttl=3600)
def ensure_structure(_spreadsheet):
    existing_sheets = [s.title for s in _spreadsheet.worksheets()]
    
    for name, headers in STRUCTURE.items():
        if name not in existing_sheets:
            _spreadsheet.add_worksheet(title=name, rows=100, cols=20)
            sh = _spreadsheet.worksheet(name)
            sh.append_row(headers)
        else:
            sh = _spreadsheet.worksheet(name)
            # Verificar si los encabezados coinciden. Si no, actualizarlos para que coincidan con la app.
            try:
                current_headers = sh.row_values(1)
                if not current_headers or current_headers != headers:
                    # Si la hoja está vacía o los encabezados no coinciden, los corregimos
                    # Esto asegura que la app vea las columnas con los nombres correctos
                    if not current_headers:
                        sh.append_row(headers)
                    else:
                        # Si hay datos pero los encabezados están mal, actualizamos la primera fila
                        # Usamos update con un rango para asegurar que sobreescribimos los viejos
                        range_end = chr(64 + len(headers)) + "1" # A1:F1 etc
                        sh.update(f"A1:{range_end}", [headers])
            except Exception as e:
                print(f"Error verificando estructura de {name}: {e}")
    
    # Inicializar socios si no existen
    s_sheet = _spreadsheet.worksheet("Socios")
    if len(s_sheet.get_all_values()) <= 1:
        base_socios = [
            ["S001", "Socio 1 Wilches"],
            ["S002", "Socio 2 Pablo"]
        ]
        s_sheet.append_rows(base_socios)
    
    # Inicializar productos si no existen
    p_sheet = _spreadsheet.worksheet("Productos")
    if len(p_sheet.get_all_values()) <= 1:
        p_sheet.update('A1:E5', [
            ["ID_Producto", "Nombre", "Unidad", "Precio_Costo", "Precio_Venta"],
            ["DVT01", "Golf Matt", "Unidad", 0, 450],
            ["DVT02", "Tee Strike", "M2", 0, 130],
            ["DVT03", "Putting green", "M2", 0, 130],
            ["DVT04", "Putting matt", "Unidad", 0, 100]
        ])

if client:
    spreadsheet = client
    try:
        # --- CONFIGURACIÓN DE ESTRUCTURA ---
        ensure_structure(spreadsheet)

        if menu == "Clientes":
            st.title("👥 Gestión de Clientes")
            sheet = spreadsheet.worksheet("Clientes")
            
            # Leer datos con la nueva función robusta
            df_clientes = get_sheet_df("Clientes")
            
            # Formulario para nuevo cliente
            with st.expander("➕ Agregar Nuevo Cliente"):
                with st.form("nuevo_cliente"):
                    col1, col2 = st.columns(2)
                    with col1:
                        nombre = st.text_input("Nombre o Razón Social")
                        id_c = st.text_input("ID Cliente (Opcional, se genera solo si está vacío)")
                        cuit = st.text_input("CUIT")
                    with col2:
                        dir = st.text_input("Dirección")
                        tel = st.text_input("Teléfono")
                        mail = st.text_input("Mail")
                    
                    submit = st.form_submit_button("Guardar Cliente")
                    
                    if submit:
                        if nombre:
                            if not id_c:
                                id_c = f"C{len(df_clientes) + 1:03d}"
                            sheet.append_row([id_c, nombre, dir, tel, mail, cuit])
                            st.cache_data.clear()
                            st.success(f"Cliente {nombre} guardado exitosamente!")
                            st.rerun()
                        else:
                            st.warning("Por favor completa al menos el Nombre.")

            # Mostrar tabla de clientes
            st.subheader("Lista de Clientes")
            if not df_clientes.empty:
                st.dataframe(df_clientes, use_container_width=True)
            else:
                st.info("No hay clientes registrados aún.")

        elif menu == "Productos":
            st.title("⛳ Gestión de Productos")
            sheet = spreadsheet.worksheet("Productos")
            df_prod = get_sheet_df("Productos")

            st.write("A continuación puedes actualizar los precios de tus productos fijos.")
            
            if not df_prod.empty:
                # Usar un editor de datos de Streamlit para actualizar precios
                edited_df = st.data_editor(
                    df_prod,
                    column_config={
                        "ID_Producto": st.column_config.TextColumn(disabled=True),
                        "Nombre": st.column_config.TextColumn(disabled=True),
                        "Unidad": st.column_config.TextColumn(disabled=True),
                        "Precio_Costo": st.column_config.NumberColumn(format="$%.2f"),
                        "Precio_Venta": st.column_config.NumberColumn(format="$%.2f"),
                    },
                    hide_index=True,
                    use_container_width=True
                )
                
                if st.button("Guardar Cambios de Precios"):
                    # Actualizar toda la hoja con los nuevos datos
                    # (Más simple para 4 productos)
                    sheet.update([df_prod.columns.values.tolist()] + edited_df.values.tolist())
                    st.cache_data.clear()
                    st.success("Precios actualizados correctamente!")
                    st.rerun()
            else:
                st.info("Inicializando productos...")

        elif menu == "Caja Socios":
            st.title("💰 Caja y Corriente de Socios")
            
            # Leer datos necesarios con la nueva función robusta
            df_pedid = get_sheet_df("Pedidos")
            df_detal = get_sheet_df("Pedidos_Detalle")
            df_produ = get_sheet_df("Productos")
            df_gasto = get_sheet_df("Gastos")
            df_socio = get_sheet_df("Socios")
            df_retir = get_sheet_df("Retiros_Socios")

            # --- CÁLCULO DE GANANCIA DISPONIBLE ---
            # Ingresos Reales (Lo que se cobró efectivamente)
            ingresos_reales = df_pedid["Monto_Pagado"].sum() if not df_pedid.empty else 0
            
            # Gastos Totales
            gastos_totales = df_gasto["Monto"].sum() if not df_gasto.empty else 0
            
            # Caja Actual Bruta (Disponible para socios)
            caja_disponible = ingresos_reales - gastos_totales
            
            st.metric("Caja Total Disponible (Ventas Cobradas - Gastos)", f"${caja_disponible:,.2f}")
            
            # --- CUENTA CORRIENTE POR SOCIO ---
            st.subheader("Estado de Cuentas por Socio")
            
            # Suponemos división 50/50. Podrías cambiarlo luego.
            ganancia_por_socio = caja_disponible / 2
            
            cols = st.columns(len(df_socio))
            for i, row in df_socio.iterrows():
                with cols[i]:
                    socio_id = row["ID_Socio"]
                    socio_nombre = row["Nombre"]
                    
                    # 1. Cuánto cobró este socio (Pedidos)
                    # El campo se llama 'Socio_Responsable' en Pedidos
                    # Usamos el nombre del socio para comparar (ej: "Socio 1 Wilches")
                    cobros_socio = 0
                    if not df_pedid.empty:
                        # Buscar coincidencias por nombre (que es lo que guardamos)
                        # El socio_nombre en la tabla Socios es "Socio 1", pero en el selectbox pusimos "Socio 1 Wilches" 
                        # Nota: En el selectbox de pedidos pusimos ["Socio 1 Wilches", "Socio 2 Pablo"]
                        # Debemos ser cuidadosos con la comparación.
                        # Una opción es buscar si el nombre corto está contenido en el nombre guardado.
                        cobros_socio = df_pedid[df_pedid["Socio_Responsable"].str.contains(socio_nombre, na=False)]["Monto_Pagado"].astype(float).sum()
                    
                    # 2. Cuánto gastó este socio (Gastos)
                    gastos_socio = 0
                    if not df_gasto.empty:
                        gastos_socio = df_gasto[df_gasto["Socio"].str.contains(socio_nombre, na=False)]["Monto"].astype(float).sum()

                    # 3. Cuánto retiró este socio (Retiros_Socios)
                    total_retirado = 0
                    if not df_retir.empty:
                        total_retirado = df_retir[df_retir["ID_Socio"] == socio_id]["Monto"].astype(float).sum()
                    
                    # El saldo a favor se basa en la caja común (50/50) menos lo que ya retiró
                    # Pero el usuario quiere ver "quién cobra y quién gasta"
                    # Mapear nombres si están en formato viejo
                    display_nombre = "Socio 1 Wilches" if "Socio 1" in socio_nombre else ("Socio 2 Pablo" if "Socio 2" in socio_nombre else socio_nombre)
                    
                    st.info(f"**🟢 {display_nombre}**")
                    st.write(f"💵 Cobros realizados: **${cobros_socio:,.2f}**")
                    st.write(f"💸 Gastos realizados: **${gastos_socio:,.2f}**")
                    st.divider()
                    st.write(f"💰 Retiros realizados: **${total_retirado:,.2f}**")
                    
                    # Saldo Neto asignado (simplificado 50/50 de la ganancia neta total)
                    saldo_disponible_socio = ganancia_por_socio - total_retirado
                    st.success(f"**Saldo a Favor: ${saldo_disponible_socio:,.2f}**")

            # --- REGISTRAR RETIRO ---
            with st.expander("💸 Registrar Retiro de Socio"):
                with st.form("nuevo_retiro"):
                    socio_opcion = st.selectbox("Socio", df_socio["Nombre"].tolist())
                    monto_ret = st.number_input("Monto a retirar", min_value=0.0)
                    fecha_ret = st.date_input("Fecha", value=pd.to_datetime("today"))
                    concepto_ret = st.text_input("Concepto (ej: Adelanto, Pago mensual)")
                    
                    if st.form_submit_button("Confirmar Retiro"):
                        id_s = df_socio[df_socio["Nombre"] == socio_opcion]["ID_Socio"].values[0]
                        new_id = f"R{len(df_retir) + 1:03d}"
                        spreadsheet.worksheet("Retiros_Socios").append_row([
                            new_id, id_s, str(fecha_ret), monto_ret, concepto_ret
                        ])
                        st.cache_data.clear()
                        st.success("Retiro registrado correctamente!")
                        st.rerun()

        elif menu == "Dashboard":
            st.title("⛳ DIVOT DEALS")
            st.subheader("Resumen General del Negocio")
            
            # Cargar todos los datos para el resumen con la nueva función robusta
            df_clientes = get_sheet_df("Clientes")
            df_pedidos = get_sheet_df("Pedidos")
            df_detalle = get_sheet_df("Pedidos_Detalle")
            df_productos = get_sheet_df("Productos")
            
            # 1. Métricas Principales
            col1, col2, col3 = st.columns(3)
            with col1:
                total_clientes = len(df_clientes)
                st.metric("Cantidad de Clientes", total_clientes)
            with col2:
                total_pedidos = len(df_pedidos)
                st.metric("Total de Pedidos", total_pedidos)
            with col3:
                venta_total = df_pedidos["Monto_Total"].sum() if not df_pedidos.empty else 0
                st.metric("Venta Total Acumulada", f"${venta_total:,.2f}")
            
            st.divider()
            
            col_l, col_r = st.columns(2)
            
            with col_l:
                st.subheader("🛒 Últimos Pedidos")
                if not df_pedidos.empty:
                    try:
                        # Mostrar los últimos 5 pedidos
                        ultimos_p = df_pedidos.sort_values(by="Fecha", ascending=False).head(5)
                        # Unir con clientes para mostrar el nombre en lugar del ID
                        if not df_clientes.empty:
                            resumen_p = ultimos_p.merge(df_clientes[["ID_Cliente", "Nombre_Razon_Social"]], on="ID_Cliente", how="left")
                        else:
                            resumen_p = ultimos_p
                            resumen_p["Nombre_Razon_Social"] = "Cliente Desconocido"
                        
                        cols_mostrar = [c for c in ["Fecha", "Nombre_Razon_Social", "Monto_Total", "Estado"] if c in resumen_p.columns]
                        st.dataframe(resumen_p[cols_mostrar], hide_index=True, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error procesando pedidos: {e}")
                else:
                    st.info("No hay pedidos registrados.")

            with col_r:
                st.subheader("🔝 Top 4 Productos más vendidos")
                if not df_detalle.empty and not df_productos.empty:
                    try:
                        # Agrupar por producto y sumar cantidad
                        top_prod = df_detalle.groupby("ID_Producto")["Cantidad"].sum().sort_values(ascending=False).head(4).reset_index()
                        # Unir con la tabla de productos para tener los nombres
                        top_prod = top_prod.merge(df_productos[["ID_Producto", "Nombre"]], on="ID_Producto")
                        
                        for i, row in top_prod.iterrows():
                            st.write(f"**{i+1}. {row['Nombre']}**: {row['Cantidad']} unidades")
                    except Exception as e:
                        st.error(f"Error calculando top productos: {e}")
                else:
                    st.info("No hay datos de ventas aún.")

        elif menu == "Pedidos":
            st.title("🛍️ Arma el Pedido")
            
            # Cargar datos
            df_clientes = get_sheet_df("Clientes")
            df_productos = get_sheet_df("Productos")
            df_pedidos_existentes = get_sheet_df("Pedidos")

            if df_clientes.empty or df_productos.empty:
                st.warning("Se necesitan Clientes y Productos para armar un pedido.")
            else:
                # 1. Selección de Cliente
                st.subheader("👤 Cliente")
                clientes_list = df_clientes.apply(lambda x: f"{x['Nombre_Razon_Social']} [{x['ID_Cliente']}]", axis=1).tolist()
                cliente_sel = st.selectbox("Seleccionar Cliente del sistema", clientes_list, key="sel_cliente_pedido")
                id_cliente = cliente_sel.split("[")[-1].replace("]", "") if "[" in cliente_sel else cliente_sel

                st.divider()

                # 2. Arma el Pedido (Lógica de Carrito)
                st.subheader("📋 Arma el pedido")
                
                if 'carrito_pedido' not in st.session_state:
                    st.session_state.carrito_pedido = []

                # Fila para agregar producto
                col_p, col_c, col_pr, col_btn = st.columns([3, 1, 1, 1])
                
                with col_p:
                    prod_names = df_productos["Nombre"].tolist()
                    producto_nombre = st.selectbox("Producto", prod_names, key="add_prod_name")
                
                with col_c:
                    cantidad = st.number_input("Cantidad", min_value=0.1, value=1.0, step=1.0, key="add_prod_cant")
                
                with col_pr:
                    # Traer el precio base del producto seleccionado
                    precio_base = float(df_productos[df_productos["Nombre"] == producto_nombre]["Precio_Venta"].values[0])
                    precio_final = st.number_input("Precio USD", min_value=0.0, value=precio_base, key="add_prod_price")
                
                with col_btn:
                    st.write("") # Espacio
                    st.write("") # Espacio
                    if st.button("➕ Agregar"):
                        # Obtener ID_Producto
                        id_p = df_productos[df_productos["Nombre"] == producto_nombre]["ID_Producto"].values[0]
                        
                        st.session_state.carrito_pedido.append({
                            "ID_Producto": id_p,
                            "Producto": producto_nombre,
                            "Cantidad": cantidad,
                            "Precio": precio_final,
                            "Total": cantidad * precio_final
                        })
                        st.rerun()

                # Mostrar Tabla del pedido actual
                if st.session_state.carrito_pedido:
                    df_carrito = pd.DataFrame(st.session_state.carrito_pedido)
                    st.table(df_carrito[["Producto", "Cantidad", "Precio", "Total"]])
                    
                    total_final = df_carrito["Total"].sum()
                    st.markdown(f"### Total del Pedido: **USD {total_final:,.2f}**")
                    
                    if st.button("🗑️ Vaciar Pedido"):
                        st.session_state.carrito_pedido = []
                        st.rerun()

                    st.divider()

                    # 3. Datos Finales y Guardar
                    with st.form("confirmar_guardado"):
                        st.subheader("📝 Finalizar y Guardar")
                        col_f1, col_f2 = st.columns(2)
                        with col_f1:
                            cobro_hoy = st.number_input("Cobro realizado hoy (USD)", min_value=0.0, max_value=float(total_final), value=0.0)
                        with col_f2:
                            socio_cobro = st.selectbox("Socio que cobra", ["Socio 1 Wilches", "Socio 2 Pablo"])
                        
                        obs = st.text_area("Observaciones / Elementos necesarios", placeholder="Ej: entrega inmediata, seña recibida...")
                        
                        if st.form_submit_button("💾  GUARDAR PEDIDO"):
                            # Generar ID
                            id_pedido = f"ORD{len(df_pedidos_existentes) + 1:04d}"
                            fecha_hoy = str(pd.to_datetime("today").date())
                            
                            try:
                                # Guardar en Pedidos (Enviar 13 valores para coincidir con la estructura)
                                # ["ID_Pedido", "ID_Cliente", "Fecha", "Estado", "Monto_Total", "Monto_Pagado", "Observaciones", "Materiales", "Obreros", "Fecha_Trabajo", "Fecha_Entrega", "Socio_Responsable", "Personal_Asignado"]
                                row_pedido = [
                                    id_pedido, id_cliente, fecha_hoy, "Pendiente", total_final, cobro_hoy, obs,
                                    "", "", "", "", socio_cobro, ""
                                ]
                                spreadsheet.worksheet("Pedidos").append_row(row_pedido)
                                
                                # Guardar en Pedidos_Detalle
                                detalle_rows = []
                                for item in st.session_state.carrito_pedido:
                                    detalle_rows.append([
                                        f"{id_pedido}_{item['ID_Producto']}", id_pedido, item["ID_Producto"], item["Cantidad"], item["Precio"]
                                    ])
                                spreadsheet.worksheet("Pedidos_Detalle").append_rows(detalle_rows)
                                
                                st.success(f"¡Pedido {id_pedido} guardado con éxito!")
                                st.session_state.carrito_pedido = []
                                st.cache_data.clear()
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error al guardar: {e}")
                else:
                    st.info("Agrega productos arriba para armar el pedido.")

        elif menu == "Logística/Pedidos":
            st.title("🚚 Gestión y Logística de Pedidos")
            
            df_pedidos = get_sheet_df("Pedidos")
            df_clientes = get_sheet_df("Clientes")
            
            if df_pedidos.empty:
                st.info("No hay pedidos registrados para gestionar.")
            else:
                # Calcular Resta Pagar y asegurar tipos numéricos
                df_pedidos["Monto_Total"] = pd.to_numeric(df_pedidos["Monto_Total"], errors='coerce').fillna(0)
                df_pedidos["Monto_Pagado"] = pd.to_numeric(df_pedidos["Monto_Pagado"], errors='coerce').fillna(0)
                df_pedidos["Resta_Pagar"] = df_pedidos["Monto_Total"] - df_pedidos["Monto_Pagado"]

                # Unir con clientes para ver el nombre
                if not df_clientes.empty:
                    df_gest = df_pedidos.merge(df_clientes[["ID_Cliente", "Nombre_Razon_Social"]], on="ID_Cliente", how="left")
                else:
                    df_gest = df_pedidos
                    df_gest["Nombre_Razon_Social"] = "Desconocido"
                
                # Intentar traer detalle de productos para "Materiales"
                try:
                    df_detalle = get_sheet_df("Pedidos_Detalle")
                    df_productos = get_sheet_df("Productos")
                    if not df_detalle.empty and not df_productos.empty:
                        df_det_prod = df_detalle.merge(df_productos[["ID_Producto", "Nombre"]], on="ID_Producto", how="left")
                        # Agrupar productos por pedido: "2x Golf Matt, 1x Tee Strike"
                        def format_item(row):
                            try:
                                q = float(row['Cantidad'])
                                return f"{row['Nombre']} ({int(q)})"
                            except:
                                return f"{row['Nombre']} ({row['Cantidad']})"
                        
                        df_det_prod["Detalle_Str"] = df_det_prod.apply(format_item, axis=1)
                        resumen_pedidos = df_det_prod.groupby("ID_Pedido")["Detalle_Str"].apply(lambda x: " | ".join(x)).reset_index()
                        resumen_pedidos.columns = ["ID_Pedido", "Materiales_Detalle"]
                        df_gest = df_gest.merge(resumen_pedidos, on="ID_Pedido", how="left")
                        # Priorizar el detalle de productos si existe, si no mantener lo que haya en la columna Materiales
                        df_gest["Materiales"] = df_gest["Materiales_Detalle"].fillna(df_gest["Materiales"]).fillna("")
                except:
                    pass

                # Reordenar y renombrar columnas para la vista del usuario
                cols_vista = {
                    "ID_Pedido": "ID",
                    "Nombre_Razon_Social": "Cliente",
                    "Fecha": "Fecha",
                    "Estado": "Situación",
                    "Materiales": "Materiales (Productos)",
                    "Obreros": "Personal necesario",
                    "Observaciones": "Elementos necesarios",
                    "Monto_Pagado": "Monto Pagado Hoy",
                    "Resta_Pagar": "Resta pagar",
                    "Fecha_Trabajo": "Fecha Trabajo",
                    "Personal_Asignado": "Personal Asignado",
                    "Socio_Responsable": "Socio Responsable",
                    "Fecha_Entrega": "Fecha Entrega",
                    "Monto_Total": "Total USD"
                }
                
                # Columnas a mostrar en el editor
                cols_mostrar = [
                    "ID_Pedido", "Nombre_Razon_Social", "Fecha", "Estado", 
                    "Materiales", "Obreros", "Observaciones", 
                    "Monto_Pagado", "Resta_Pagar", "Fecha_Trabajo", 
                    "Fecha_Entrega", "Socio_Responsable", "Personal_Asignado"
                ]
                
                st.write("Gestioná tus pedidos por estado. Editá directamente en las tablas.")

                tab1, tab2, tab3 = st.tabs(["⏳ Pendientes", "✅ Entregados", "❌ Anulados"])
                
                def render_gest_table(df_subset, key):
                    return st.data_editor(
                        df_subset[cols_mostrar],
                        column_config={
                            "ID_Pedido": st.column_config.TextColumn("ID", disabled=True),
                            "Nombre_Razon_Social": st.column_config.TextColumn("Cliente", disabled=True),
                            "Fecha": st.column_config.TextColumn("Fecha", disabled=True),
                            "Estado": st.column_config.SelectboxColumn(
                                "Situación",
                                options=["Pendiente", "En Preparación", "Listo para Entrega", "Entregado", "Cancelado"]
                            ),
                            "Materiales": st.column_config.TextColumn("Materiales (Productos)"),
                            "Obreros": st.column_config.NumberColumn("Personal necesario", min_value=0, step=1),
                            "Observaciones": st.column_config.TextColumn("Elementos necesarios"),
                            "Monto_Pagado": st.column_config.NumberColumn("Monto Pagado hasta el momento", min_value=0.0, format="$%.2f"),
                            "Resta_Pagar": st.column_config.NumberColumn("Resta pagar", disabled=True, format="$%.2f"),
                            "Fecha_Trabajo": st.column_config.TextColumn("Fecha Trabajo"),
                            "Fecha_Entrega": st.column_config.TextColumn("Fecha Entrega"),
                            "Personal_Asignado": st.column_config.TextColumn("Personal Asignado"),
                            "Socio_Responsable": st.column_config.SelectboxColumn(
                                "Socio que cobra",
                                options=["Socio 1 Wilches", "Socio 2 Pablo"]
                            ),
                        },
                        hide_index=True,
                        use_container_width=True,
                        key=key
                    )

                with tab1:
                    df_p = df_gest[~df_gest["Estado"].isin(["Entregado", "Cancelado"])]
                    edited_p = render_gest_table(df_p, "editor_pendientes")
                
                with tab2:
                    df_e = df_gest[df_gest["Estado"] == "Entregado"]
                    edited_e = render_gest_table(df_e, "editor_entregados")
                
                with tab3:
                    df_a = df_gest[df_gest["Estado"] == "Cancelado"]
                    edited_a = render_gest_table(df_a, "editor_anulados")

                if st.button("💾 Guardar Cambios Logísticos"):
                    try:
                        # Combinar ediciones de todos los tabs (usamos el ID_Pedido como ancla)
                        # Nota: En Streamlit, st.data_editor devuelve el dataframe completo EDITADO
                        # Pero como tenemos 3 editores, necesitamos rastrear cuál se usó o simplemente priorizar cambios.
                        # Una forma sencilla es concatenarlos y quitar duplicados por ID, pero el editor devuelve TODO el df filtrado.
                        
                        # Sin embargo, como el usuario solo puede estar en un TAB a la vez al hacer click en el botón (que está afuera),
                        # lo ideal sería consolidar. Si editó en varios, st.session_state guarda los estados.
                        # Para simplificar, asumimos que el usuario guarda lo que ve o consolidamos:
                        
                        # Consolidación simple:
                        all_edited = pd.concat([edited_p, edited_e, edited_a]).drop_duplicates(subset="ID_Pedido", keep="last")
                        
                        sheet_cols = [
                            "ID_Pedido", "ID_Cliente", "Fecha", "Estado", 
                            "Monto_Total", "Monto_Pagado", "Observaciones", 
                            "Materiales", "Obreros", "Fecha_Trabajo", 
                            "Fecha_Entrega", "Socio_Responsable", "Personal_Asignado"
                        ]
                        
                        # Recuperar ID_Cliente y Monto_Total original del df_pedidos (columnas que no están en el editor)
                        # También traemos Monto_Pagado original por si no se editó (aunque aquí se edita)
                        df_to_save = all_edited.merge(df_pedidos[["ID_Pedido", "ID_Cliente", "Monto_Total"]], on="ID_Pedido", how="left")
                        
                        # Limpiar datos para que sean compatibles con JSON (evitar NaNs en celdas numéricas)
                        for col in sheet_cols:
                            if col not in df_to_save.columns:
                                df_to_save[col] = ""
                        
                        # Asegurar que Monto_Total y Monto_Pagado no tengan NaNs
                        df_to_save["Monto_Total"] = pd.to_numeric(df_to_save["Monto_Total"], errors='coerce').fillna(0)
                        df_to_save["Monto_Pagado"] = pd.to_numeric(df_to_save["Monto_Pagado"], errors='coerce').fillna(0)
                        df_to_save = df_to_save.fillna("") # El resto a strings vacíos
                        
                        data_to_update = [sheet_cols] + df_to_save[sheet_cols].values.tolist()
                        spreadsheet.worksheet("Pedidos").update(data_to_update)
                        st.cache_data.clear()
                        st.success("Logística actualizada correctamente!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al guardar: {e}")

        elif menu == "Gastos":
            st.title("💸 Registro de Gastos")
            sheet = spreadsheet.worksheet("Gastos")
            df_gastos = get_sheet_df("Gastos")

            with st.form("nuevo_gasto"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    fecha_g = st.date_input("Fecha", value=pd.to_datetime("today"))
                    cat_g = st.selectbox("Categoría", ["Alquiler", "Servicios", "Materiales", "Marketing", "Otros"])
                with col2:
                    monto_g = st.number_input("Monto", min_value=0.0)
                with col3:
                    socio_g = st.selectbox("Socio que gasta", ["Socio 1 Wilches", "Socio 2 Pablo"])
                
                desc_g = st.text_input("Descripción / Detalle")
                
                if st.form_submit_button("Registrar Gasto"):
                    if monto_g > 0:
                        id_g = f"G{len(df_gastos) + 1:03d}"
                        sheet.append_row([id_g, str(fecha_g), cat_g, desc_g, monto_g, socio_g])
                        st.cache_data.clear()
                        st.success("Gasto registrado exitosamente!")
                        st.rerun()
                    else:
                        st.warning("El monto debe ser mayor a 0.")

            st.subheader("Historial de Gastos")
            if not df_gastos.empty:
                st.dataframe(df_gastos.sort_values(by="Fecha", ascending=False), use_container_width=True)
            else:
                st.info("No hay gastos registrados.")

    except gspread.exceptions.WorksheetNotFound:
        st.error("Una de las hojas no existe. Asegúrate de que las hojas (Clientes, Productos, etc.) estén creadas.")
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("Esperando configuración de credenciales...")

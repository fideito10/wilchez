import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

def init_sheets():
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds_dict = st.secrets["gcp_service_account"]
        credentials = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(credentials)
        
        SHEET_URL = "https://docs.google.com/spreadsheets/d/1gX16hMqj7xYPlDsNJeeNaQu8sz_2VR-SNDlZedm2vWM/edit"
        spreadsheet = client.open_by_url(SHEET_URL)
        
        structure = {
            "Clientes": ["ID_Cliente", "Nombre_Razon_Social", "Dirección", "Teléfono", "Mail", "CUIT"],
            "Productos": ["ID_Producto", "Nombre", "Unidad", "Precio_Costo", "Precio_Venta"],
            "Pedidos": ["ID_Pedido", "ID_Cliente", "Fecha", "Estado", "Monto_Total", "Monto_Pagado", "Observaciones", "Materiales", "Obreros"],
            "Pedidos_Detalle": ["ID_Detalle", "ID_Pedido", "ID_Producto", "Cantidad", "Precio_Historico"],
            "Tareas": ["ID_Tarea", "ID_Pedido", "Descripcion", "Fecha_Limite", "Estado"],
            "Gastos": ["ID_Gasto", "Fecha", "Categoria", "Descripcion", "Monto"]
        }
        
        for sheet_name, headers in structure.items():
            try:
                sheet = spreadsheet.worksheet(sheet_name)
                # Si está vacía, poner encabezados
                if not sheet.get_all_values():
                    sheet.append_row(headers)
                    print(f"Encabezados creados en {sheet_name}")
            except gspread.exceptions.WorksheetNotFound:
                print(f"Error: La hoja {sheet_name} no existe.")
                
    except Exception as e:
        print(f"Error en inicialización: {e}")

if __name__ == "__main__":
    # Este script se usaría internamente o desde la app
    pass

# ⛳ Manual de Usuario: Divot Deals - Gestión de Golf

¡Bienvenido al sistema de gestión de **Divot Deals**! Esta herramienta ha sido diseñada para optimizar la administración de tus clientes, ventas, inventario y finanzas de manera sencilla y profesional.

---

## 1. Acceso al Sistema

Para ingresar al sistema, utiliza las siguientes credenciales:

*   **Usuario:** `Wilches1`
*   **Contraseña:** `Soygordo`

> [!TIP]
> Puedes acceder desde cualquier navegador moderno. La interfaz cuenta con un diseño oscuro (Dark Mode) optimizado para una mejor visualización de datos.

---

## 2. Navegación Principal

En la barra lateral izquierda encontrarás el menú "Ir a:", donde podrás navegar entre los siguientes módulos:

*   **Dashboard:** Resumen general del negocio.
*   **Clientes:** Gestión de tu base de contactos.
*   **Productos:** Actualización de precios de stock fijo.
*   **Pedidos:** Creación de nuevas órdenes de venta.
*   **Logística/Pedidos:** Seguimiento y gestión del estado de los trabajos.
*   **Gastos:** Registro de salidas de dinero corporativas.
*   **Caja Socios:** Control financiero detallado de cada socio.

---

## 3. Módulos en Detalle

### 📊 Dashboard (Tablero de Control)
Es la pantalla de inicio. Aquí verás:
*   Métricas clave (Total de clientes, pedidos y ventas acumuladas).
*   Lista de los últimos 5 pedidos realizados.
*   Ranking de los productos más vendidos.

### 👥 Clientes
Utiliza este módulo para llevar un registro ordenado de tus clientes.
1.  Haz clic en **"Agregar Nuevo Cliente"**.
2.  Completa los datos (Nombre/Razón Social, CUIT, Dirección, etc.).
3.  El sistema generará automáticamente un ID único si lo dejas vacío.

### 🛍️ Arma el Pedido (Ventas)
Aquí es donde registras cada venta nueva:
1.  **Selecciona un cliente** del menú desplegable.
2.  **Agrega productos:** Elige el producto, define la cantidad y el precio (puedes ajustar el precio manualmente si es una oferta especial).
3.  **Finaliza:** Indica cuánto entrega el cliente hoy (cobro inicial), quién es el socio que recibe el dinero y agrega cualquier nota necesaria en "Elementos necesarios".

### 🚚 Logística / Pedidos
Este es el corazón operativo. Aquí puedes:
*   Cambiar la **Situación** del pedido: `Pendiente`, `En Preparación`, `Listo para Entrega`, `Entregado` o `Cancelado`.
*   Asignar **Personal** y fechas de trabajo/entrega.
*   Actualizar el **Monto Pagado** a medida que el cliente completa el pago.
*   **IMPORTANTE:** Siempre haz clic en **"Guardar Cambios Logísticos"** para que la información se guarde en la base de datos general.

### 💰 Caja Socios
Control financiero transparente:
*   **Ganancia Disponible:** Muestra cuánto dinero hay realmente (Ingresos cobrados - Gastos realizados).
*   **Cuentas por Socio:** El sistema calcula automáticamente el saldo de cada socio (basado en un esquema 50/50).
*   **Registrar Retiro:** Cada vez que un socio retire dinero, debe registrarlo aquí con el concepto correspondiente.

---

## 4. Mantenimiento de Datos

Si sientes que la información no está actualizada (por ejemplo, después de un cambio manual en Google Sheets), utiliza el botón:
*   **🔄 Refrescar Datos** (en la barra lateral).

> [!IMPORTANT]
> Los precios de los productos pueden actualizarse en el módulo **"Productos"**. Solo cambia el valor en la tabla y presiona **"Guardar Cambios de Precios"**.

---

*Manual generado para Divot Deals - Febrero 2026*

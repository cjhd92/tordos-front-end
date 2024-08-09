import streamlit as st
from fpdf import FPDF

def main():
    forma_de_pago ='Sin definir'
    descripcion = 'Toldo telón balcon L-2,00 x B-2,80'

    unidad = 1
    precio = 20
    total = 360


    st.title("Hoja de Pedido")

    fecha = st.date_input("Fecha:")

    # Crear columnas para la sección de información del cliente
    col1, col2 = st.columns(2)
    with col1:
        
        cliente = st.text_input("Cliente:")
        localidad = st.text_input("Localidad:")
        telefono = st.text_input("Teléfono:")
        
    
    with col2:
        nif = st.text_input("N.I.F:")
        fax = st.text_input("Fax:")
        referencia = st.text_input("Ref Pedido:")
    
    # Crear una sección para Modelo Toldo
    st.header("Modelo Toldo")
    #st.caption("Vertical")  # Texto pequeño debajo del encabezado
    st.subheader("**Verticales**")  # Subtítulo más grande y en negrita
    
    
    cols = st.columns(4)  # Crear 4 columnas para los checkboxes
    with cols[0]:
        lor = st.checkbox("Lor")
    with cols[1]:
        sil = st.checkbox("Sil")
    with cols[2]:
        tambre = st.checkbox("Tambre")
    with cols[3]:
        mao = st.checkbox("Mao")

        
    
    # Verticales Nexus
    #st.header("Verticales Nexus")
    st.subheader("**Verticales Nexus**")  # Subtítulo más grande y en negrita
 
    cols2 = st.columns(5)  # Crear 5 columnas para los checkboxes
    with cols2[0]:
        nx_80 = st.checkbox("80")
    with cols2[1]:
        nx_100 = st.checkbox("100")
    with cols2[2]:
        nx_130 = st.checkbox("130")
    with cols2[3]:
        cuadrado = st.checkbox("Cuadrado")
    with cols2[4]:
        redondo = st.checkbox("Redondo")
    with cols2[0]:
        cable = st.checkbox("Cable")
    with cols2[1]:
        guia = st.checkbox("Guía 30x43")
    with cols2[2]:
        zip = st.checkbox("Zip")

    # Botón para enviar el pedido y generar PDF
    if st.button("Enviar Pedido"):
        if any([cliente, nif, localidad, telefono, referencia]):
            pdf = FPDF()
            pdf.add_page()
            
            # Configuración de la fuente
            pdf.set_font("Arial", size=12)

            # Encabezado
            pdf.image('C:/Equipo/Curso/Jorge/Manejo de datos/logo.png', 10, 8, 33,25)  # Asegúrate de usar la ruta correcta al logo
            pdf.cell(200, 10, txt=f"Presupuesto (0062.3/2024)", ln=True, align='C')
            #pdf.cell(200, 10, txt=f"Presupuesto (0062.3/2024) - {fecha.strftime('%d/%m/%Y')}", ln=True, align='C')

            # Información del presupuestador y del cliente
            pdf.set_xy(10, 40)

            

            pdf.cell(100, 10, txt=f"Solares Valencia (Empresa)", ln=True)

           
            pdf.cell(100, 10, txt=f"Cliente: {cliente}                               Presupuestar : Yudith/Salva", ln=True)
            pdf.cell(100, 10, txt=f"NIF: {nif}", ln=True)
            pdf.cell(100, 10, txt=f"Dirección: {localidad}", ln=True)
            pdf.cell(100, 10, txt=f"Teléfono: {telefono}", ln=True)
            pdf.cell(100, 10, txt=f"Fax: {fax}", ln=True)
            pdf.cell(100, 10, txt=f"Ref Pedido: {referencia}", ln=True)
            #pdf.cell(100, 10, txt=f"Forma de pago: {forma_de_pago}", ln=True)

            pdf.set_font("Arial", size=12)

            # Añadir celda para "Fecha de presupuesto"
            pdf.cell(130, 10, 'Fecha de presupuesto 11/07/2024', 1, 0, 'L')  # 130 mm de ancho, alineación izquierda, con borde

            # Añadir celda para "Forma de pago"
            pdf.cell(60, 10, 'Forma de pago: A Definir', 1, 1, 'L')  # 60 mm de ancho, nueva línea después de esta celda


            # Tabla de productos
            pdf.cell(200, 10, txt="Descripción       UD       Precio       Total", ln=True)
            pdf.cell(200, 10, txt=f"{descripcion}       {unidad}       {precio:.2f}euros       {total:.2f}euros", ln=True)

            # Totales
            subtotal = total
            iva = subtotal * 0.21
            total_presupuesto = subtotal + iva
            pdf.cell(200, 10, txt=f"SUB-TOTAL: {subtotal:.2f}euros", ln=True)
            pdf.cell(200, 10, txt=f"IVA 21%: {iva:.2f}euros", ln=True)
            pdf.cell(200, 10, txt=f"TOTAL: {total_presupuesto:.2f}euros", ln=True)

            # IBAN para transferencias
            pdf.cell(200, 10, txt="IBAN: ES18 0127 3241 1102 0160 5004", ln=True)

            # Guardar el PDF
            pdf.output("pedido.pdf")
            st.success("Pedido enviado con éxito y PDF generado!")
            st.download_button(
                label="Descargar PDF",
                data=open("pedido.pdf", "rb"),
                file_name="pedido.pdf",
                mime="application/octet-stream"
            )
        else:
            st.error("Por favor, completa todos los campos antes de enviar.")

if __name__ == "__main__":
    main()

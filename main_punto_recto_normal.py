import streamlit as st
from decimal import Decimal
import bisect
from fpdf import FPDF
import pandas as pd
import os
#versio 1

""" 
def validar_telefono(telefono):
   
    return telefono.isdigit() and len(telefono) == 9 """

def validar_telefono(telefono):
    """Función para validar el número de teléfono con exactamente 9 dígitos."""
    import re
    # Expresión regular para permitir solo dígitos
    patron = r'^\d{9}$'
    if re.match(patron, telefono):
        return True
    return False


def seleccionar_proximo_valor_disponible(medida, valores_disponibles):
    """Encuentra el próximo valor más alto disponible si la medida exacta no está presente."""
    index = bisect.bisect_left(valores_disponibles, medida)
    if index == len(valores_disponibles):
        index -= 1  # Si es más grande que cualquier valor, use el último disponible
    return valores_disponibles[index]

def seleccionar_proximo_precio_tejadillo(medida, precios_tejadillo):
    """Determina el precio del tejadillo basado en la medida más cercana hacia arriba."""
    medidas_disponibles = sorted(precios_tejadillo.keys())
    index = bisect.bisect_left(medidas_disponibles, medida)
    if index == len(medidas_disponibles):
        index -= 1  # Si es más grande que cualquier valor, use el último disponible
    return precios_tejadillo[medidas_disponibles[index]]


def obtener_nuevo_presupuesto():
    """Lee el último presupuesto del archivo Excel y lo incrementa en 1."""
    
    #file_path = "C:/Equipo/Curso/Jorge/Manejo de datos/assets/presupuestos.xlsx"
    file_path = 'assets/presupuestos.xlsx'
    # Comprobar si el archivo existe
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        ultimo_presupuesto = df['Presupuesto'].max()
        numero = int(ultimo_presupuesto[1:])  # Obtener el número, eliminando la letra 'P'
        nuevo_presupuesto = f"P{numero + 1:03}"  # Formato P001, P002, ...
    else:
        # Si el archivo no existe, empezamos con el presupuesto 1
        nuevo_presupuesto = "P001"

    return nuevo_presupuesto

def actualizar_excel_con_presupuesto(nuevo_presupuesto):
    """Actualiza el archivo Excel con el nuevo presupuesto."""
    #file_path = "C:/Equipo/Curso/Jorge/Manejo de datos/assets/presupuestos.xlsx"
    file_path = 'assets/presupuestos.xlsx'
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
    else:
        df = pd.DataFrame(columns=['Presupuesto'])

    
    
    # Crear un nuevo DataFrame con el presupuesto a añadir
    nuevo_df = pd.DataFrame({'Presupuesto': [nuevo_presupuesto]})
    
    # Concatenar el nuevo presupuesto al DataFrame existente
    df = pd.concat([df, nuevo_df], ignore_index=True)
    
    # Guardar el DataFrame en el archivo Excel
    df.to_excel(file_path, index=False)



def main():
    # Diccionario de precios, sustituye con los valores reales de tu tabla
    precios = {
        1.50: {0.80: 370, 1.00: 400, 1.20: 408, 1.40: 434, 1.50: 460},
        1.75: {0.80: 380, 1.00: 406, 1.20: 430, 1.40: 448, 1.50: 478},
        2.00: {0.80: 394, 1.00: 424, 1.20: 438, 1.40: 464, 1.50: 488},
        2.25: {0.80: 408, 1.00: 438, 1.20: 452, 1.40: 480, 1.50: 504},
        2.50: {0.80: 440, 1.00: 476, 1.20: 494, 1.40: 526, 1.50: 556},
        2.75: {0.80: 460, 1.00: 494, 1.20: 504, 1.40: 534, 1.50: 568},
        3.00: {0.80: 468, 1.00: 504, 1.20: 514, 1.40: 548, 1.50: 582},
        3.25: {0.80: 482, 1.00: 518, 1.20: 528, 1.40: 560, 1.50: 616},
        3.50: {0.80: 494, 1.00: 530, 1.20: 544, 1.40: 580, 1.50: 628},
        3.75: {0.80: 552, 1.00: 598, 1.20: 616, 1.40: 666, 1.50: 698},
        4.00: {0.80: 572, 1.00: 600, 1.20: 626, 1.40: 670, 1.50: 708},
        4.25: {0.80: 578, 1.00: 618, 1.20: 642, 1.40: 688, 1.50: 730},
        4.50: {0.80: 584, 1.00: 626, 1.20: 652, 1.40: 696, 1.50: 738},
        4.75: {0.80: 602, 1.00: 656, 1.20: 682, 1.40: 722, 1.50: 768},
        5.00: {0.80: 656, 1.00: 704, 1.20: 744, 1.40: 794, 1.50: 846},
        5.25: {0.80: 676, 1.00: 726, 1.20: 750, 1.40: 806, 1.50: 860},
        5.50: {0.80: 704, 1.00: 760, 1.20: 782, 1.40: 834, 1.50: 880},
        5.75: {0.80: 732, 1.00: 778, 1.20: 812, 1.40: 854, 1.50: 898},
        6.00: {0.80: 780, 1.00: 838, 1.20: 884, 1.40: 914, 1.50: 936},
    }

    # Inicializar los valores en el estado de sesión si no existen
    if 'cliente' not in st.session_state:
        st.session_state.cliente = ''
    if 'localidad' not in st.session_state:
        st.session_state.localidad = ''
    if 'telefono' not in st.session_state:
        st.session_state.telefono = ''

    st.title("Hoja de Pedido para Toldos Punto Recto Normal")

    fecha = st.date_input("Fecha:")
    st.session_state.localidad = st.text_input("Dirección:", value=st.session_state.localidad)

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.cliente = st.text_input("Nombre:", value=st.session_state.cliente)

    with col2:
        st.session_state.telefono = st.text_input("Teléfono:", value=st.session_state.telefono)

    st.header("Parámetros del Toldo")
    st.subheader("**Medidas:**")
    linea_input = st.number_input("Linea (m):", min_value=1.50, step=0.1, format="%.2f")
    brazo_input = st.number_input("Brazo (m):", min_value=0.80, step=0.1, format="%.2f")

    linea = Decimal(linea_input).quantize(Decimal('0.00'))
    brazo = Decimal(brazo_input).quantize(Decimal('0.00'))

    lineas_disponibles = sorted(precios.keys())
    brazos_disponibles = sorted(next(iter(precios.values())).keys())

    linea_seleccionada = seleccionar_proximo_valor_disponible(linea, lineas_disponibles)
    brazo_seleccionado = seleccionar_proximo_valor_disponible(brazo, brazos_disponibles)

    try:
        precio = precios[linea_seleccionada][brazo_seleccionado]
        st.write(f"El precio para Linea {linea_seleccionada} m y Brazo {brazo_seleccionado} m es de EUR{precio}")
    except KeyError:
        st.error("Combinación de medidas no disponible.")

    st.subheader("**Tejadillo**")
    tejadillo = st.checkbox("Visualizar medidas del Tejadillo")
    medida_tejadillo = 0
    precio_tejadillo = 0
    if tejadillo:
        medida_tejadillo = st.number_input("Medida del Tejadillo (m):", min_value=4.00, step=0.1, format="%.2f")
        medida_tejadillo = Decimal(medida_tejadillo).quantize(Decimal('0.00'))

        precios_tejadillo = {
            4.0: 450,
            5.0: 550,
            6.0: 620,
            7.0: 700,
        }

        precio_tejadillo = seleccionar_proximo_precio_tejadillo(medida_tejadillo, precios_tejadillo)
        st.write(f"Costo del tejadillo para {medida_tejadillo} m: {precio_tejadillo} EUR")

    st.subheader("**Motores**")
    opcion_motor = st.selectbox("Motor", ["No usar Motores", "Motor Mando", "Motor Pulsador"])
    precios_motor = {"Motor Pulsador": 200, "Motor Mando": 400, "No usar Motores": 0}
    precio_motor = precios_motor[opcion_motor]
    st.write(f"Costo del Motor {opcion_motor}: {precio_motor} EUR")

    st.subheader("**Faldon**")
    faldon = st.checkbox("Visualizar medidas del Faldon")
    precio_faldon = 0
    if faldon:
        medida_faldon = st.number_input("Medida del Faldon (m):", min_value=0.00, step=0.1, format="%.2f")
        opcion_faldon = st.selectbox("Faldon", ["Faldon Recto", "Faldon Ondulado", "No usar Faldon"])
        precios_faldon = {"Faldon Recto": 0, "Faldon Ondulado": 0, "No usar Faldon": 0}
        precio_faldon = precios_faldon[opcion_faldon]
        medida_faldon = Decimal(medida_faldon).quantize(Decimal('0.00'))
        st.write(f"Costo del faldon para {medida_faldon} m es de 0 EUR")

    st.markdown("-----------------------------------------------------------------------------")

    col3, col4 = st.columns(2)

    with col3:
        precio_total = precio + precio_tejadillo + precio_motor + precio_faldon
        st.write(f"Costo del toldo sin descuento: {precio_total} EUR")
        opcion_descuento = st.selectbox("Descuento de:", ["0", "5", "10", "15", "20"])
        descuento = float(opcion_descuento) / 100
        precio_descuento = precio_total * (1 - descuento)
        st.write(f"Precio con descuento: {precio_descuento:.2f} EUR")

    if st.session_state.cliente and st.session_state.localidad and st.session_state.telefono:
        if st.button("Hacer Presupuesto"):
            # Validar el número de teléfono
            if not validar_telefono(st.session_state.telefono):
                st.error("El número de teléfono debe tener exactamente 9 dígitos.")
                return
            
            # Obtener y actualizar el presupuesto
            nuevo_presupuesto = obtener_nuevo_presupuesto()
            actualizar_excel_con_presupuesto(nuevo_presupuesto)
            
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            #pdf.image('C:/Equipo/Curso/Jorge/Manejo de datos/assets/logo.png', 10, 8, 33,25)  # Asegúrate de usar la ruta correcta al logo
                 
            pdf.image('assets/logo.png', 10, 8, 33, 25)  # Cambia la ruta de la imagen
            #pdf.cell(200, 10, txt=f"Presupuesto (0062.3/2024)", ln=True, align='C')
            pdf.cell(200, 10, txt=f"Presupuesto ({nuevo_presupuesto}/2024)", ln=True, align='C')


            pdf.set_xy(10, 40)
            left_column_width = 90
            right_column_width = 90

            pdf.set_x(10)
            pdf.cell(left_column_width, 10, 'Solares Valencia (Empresa)', 0, 1, 'L')
            pdf.cell(left_column_width, 10, 'Jorge Luis Gonzalez Ordaz', 0, 1, 'L')
            pdf.cell(left_column_width, 10, 'Ave.Cuartel 7,puerta 13. CP:46770', 0, 1, 'L')
            pdf.cell(left_column_width, 10, 'Xeraco Playa, Valencia', 0, 1, 'L')
            pdf.cell(left_column_width, 10, 'NIF: Y69018187Z', 0, 1, 'L')
            pdf.cell(left_column_width, 10, 'Telefono: +34 611 078 238', 0, 1, 'L')
        
            pdf.set_xy(100, 40)
            pdf.cell(right_column_width, 10, 'Presupuestar:', 0, 1, 'L')
            pdf.set_xy(100, 50)
            pdf.cell(right_column_width, 10, f'   {st.session_state.cliente}', 0, 1, 'L')
            pdf.set_xy(100, 60)
            pdf.cell(right_column_width, 10, f'   {st.session_state.localidad}', 0, 1, 'L')
            pdf.set_xy(100, 70)
            pdf.cell(right_column_width, 10, f'   +34 {st.session_state.telefono}', 0, 1, 'L')

            pdf.line(10, 118, 180, 118)

            pdf.set_xy(10, 125)

            left_column_width = 90
            right_column_width = 90

            pdf.cell(left_column_width, 10, f'Fecha de presupuesto:     {fecha}', 0, 1, 'L')
            pdf.set_xy(100, 125)

            pdf.cell(right_column_width, 10, 'Forma de pago:     A Definir', 0, 1, 'L')

            x_inicio = 10
            y_inicio = 150
            ancho_descripcion = 90
            ancho_ud = 20
            ancho_precio = 30
            ancho_total = 30

            pdf.set_xy(x_inicio, y_inicio)
            pdf.cell(ancho_descripcion, 10, 'DESCRIPCIÓN', border='TB', ln=0)
            pdf.cell(ancho_ud, 10, 'UD', border='TB', ln=0)
            pdf.cell(ancho_precio, 10, 'PRECIO', border='TB', ln=0)
            pdf.cell(ancho_total, 10, 'TOTAL', border='TB', ln=1)

            y_inicio += 10

            pdf.set_xy(x_inicio, y_inicio)
            pdf.cell(ancho_descripcion, 10, f'Linea: {linea} x Brazo: {brazo}', border=0, ln=0)
            pdf.cell(ancho_ud, 10, '1', border=0, ln=0)
            pdf.cell(ancho_precio, 10, f'{precio} EUR', border=0, ln=0)
            pdf.cell(ancho_total, 10, f'{precio} EUR', border=0, ln=1)

            if tejadillo:
                y_inicio += 8
                pdf.set_xy(x_inicio, y_inicio)
                pdf.cell(ancho_descripcion, 10, f'Tejadillo: {medida_tejadillo} m', border=0, ln=0)
                pdf.cell(ancho_ud, 10, '1', border=0, ln=0)
                pdf.cell(ancho_precio, 10, f'{precio_tejadillo} EUR', border=0, ln=0)
                pdf.cell(ancho_total, 10, f'{precio_tejadillo} EUR', border=0, ln=1)

            if opcion_motor != "No usar Motores":
                y_inicio += 8
                pdf.set_xy(x_inicio, y_inicio)
                pdf.cell(ancho_descripcion, 10, f'Motor: {opcion_motor}', border=0, ln=0)
                pdf.cell(ancho_ud, 10, '1', border=0, ln=0)
                pdf.cell(ancho_precio, 10, f'{precio_motor} EUR', border=0, ln=0)
                pdf.cell(ancho_total, 10, f'{precio_motor} EUR', border=0, ln=1)

            if faldon and medida_faldon > 0:
                y_inicio += 8
                pdf.set_xy(x_inicio, y_inicio)
                pdf.cell(ancho_descripcion, 10, f'Faldon: {opcion_faldon} - {medida_faldon} m', border=0, ln=0)
                pdf.cell(ancho_ud, 10, '1', border=0, ln=0)
                pdf.cell(ancho_precio, 10, f'{precio_faldon} EUR', border=0, ln=0)
                pdf.cell(ancho_total, 10, f'{precio_faldon} EUR', border=0, ln=1)

            y_inicio += 30
            pdf.line(10, y_inicio, 180, y_inicio)
            y_inicio += 8
            pdf.set_xy(x_inicio, y_inicio)
            pdf.cell(left_column_width, 10, f'Con la aprobación del presupuesto el', border=0, ln=0)
            pdf.set_xy(120, y_inicio)
            
            pdf.cell(right_column_width, 10, f'Sub - Total      {precio_descuento} EUR', border=0, ln=0)
            y_inicio += 6
            iva = precio_descuento * 0.21
            iva = round(iva, 2)
            pdf.set_xy(x_inicio, y_inicio)
            pdf.cell(left_column_width, 10, f'cliente debe abonar el 50% del monto ', border=0, ln=0)
            pdf.set_xy(120, y_inicio)
            pdf.cell(right_column_width, 10, f'IVA 21%         {iva:.2f} EUR', border=0, ln=0)
            total_con_iva = iva + precio_descuento
            total_con_iva = round(total_con_iva, 2)
            y_inicio += 6
            pdf.set_xy(x_inicio, y_inicio)
            pdf.cell(left_column_width, 10, f'total en calidadde reserva y fabricación.', border=0, ln=0)
            pdf.set_xy(120, y_inicio)
            
            pdf.cell(right_column_width, 10, f'TOTAL            {total_con_iva} EUR', border=0, ln=0)
            y_inicio += 6
            pdf.set_xy(x_inicio, y_inicio)
            pdf.cell(left_column_width, 10, f'IBAN: ES18 0182 2741 1102 0160 5004', border=0, ln=0)

            pdf.output("pedido.pdf")
            st.success("Pedido enviado con éxito y PDF generado!")
            st.download_button(
                label="Descargar PDF",
                data=open("pedido.pdf", "rb"),
                file_name="pedido.pdf",
                mime="application/octet-stream"
            )

            # Limpiar campos después de generar el presupuesto
            st.session_state.cliente = ''
            st.session_state.localidad = ''
            st.session_state.telefono = ''
        

if __name__ == "__main__":
    main()

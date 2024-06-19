# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 18:23:49 2024

@author: jperezr
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import io
import matplotlib.pyplot as plt
import base64

# Título de la Aplicación
st.title('Gestión de Redes de Contactos de LinkedIn')
st.header('Creado por: jahoperi')

# Carga de Datos
st.sidebar.header('Carga de Datos')
uploaded_file = st.sidebar.file_uploader("Sube un archivo CSV con tus contactos", type=["csv"])

# Inicializar el DataFrame
contacts = pd.DataFrame(columns=["Nombre", "Empresa", "Correo", "Teléfono", "Etiqueta", "Recordatorio", "Notas"])

if uploaded_file is not None:
    contacts = pd.read_csv(uploaded_file)

# Mostrar Contactos
st.write("### Vista de los Contactos")
st.write(contacts)

# Añadir Nuevos Contactos
st.sidebar.header('Añadir Nuevo Contacto')
new_name = st.sidebar.text_input('Nombre')
new_company = st.sidebar.text_input('Empresa')
new_email = st.sidebar.text_input('Correo')
new_phone = st.sidebar.text_input('Teléfono')
new_tag = st.sidebar.text_input('Etiqueta')
new_reminder = st.sidebar.date_input('Recordatorio', value=datetime.today())
new_note = st.sidebar.text_area('Notas')

if st.sidebar.button('Añadir Contacto'):
    new_contact = pd.DataFrame({
        "Nombre": [new_name],
        "Empresa": [new_company],
        "Correo": [new_email],
        "Teléfono": [new_phone],
        "Etiqueta": [new_tag],
        "Recordatorio": [new_reminder],
        "Notas": [new_note]
    })
    contacts = pd.concat([contacts, new_contact], ignore_index=True)
    st.write("Nuevo contacto añadido con éxito.")
    st.write(contacts)

# Buscar Contactos
st.sidebar.header('Buscar Contactos')
search_term = st.sidebar.text_input('Buscar por Nombre')
filtered_contacts = contacts[contacts['Nombre'].str.contains(search_term, case=False, na=False)]
st.write("### Resultados de la Búsqueda")
st.write(filtered_contacts)

# Editar Contactos
st.sidebar.header('Editar Contacto')
if not contacts.empty:
    contact_names = contacts['Nombre'].tolist()
    if contact_names:
        contact_to_edit = st.sidebar.selectbox('Selecciona un Contacto para Editar', contact_names)
        contact_index = contacts.index[contacts['Nombre'] == contact_to_edit].tolist()
        if contact_index:
            contact_index = contact_index[0]
            edited_name = st.sidebar.text_input('Nombre', contacts.loc[contact_index, 'Nombre'])
            edited_company = st.sidebar.text_input('Empresa', contacts.loc[contact_index, 'Empresa'])
            edited_email = st.sidebar.text_input('Correo', contacts.loc[contact_index, 'Correo'])
            edited_phone = st.sidebar.text_input('Teléfono', contacts.loc[contact_index, 'Teléfono'])
            edited_tag = st.sidebar.text_input('Etiqueta', contacts.loc[contact_index, 'Etiqueta'])
            
            # Notas con identificador único
            edited_note = st.sidebar.text_area(f'Notas_{contact_index}', contacts.loc[contact_index, 'Notas'] if 'Notas' in contacts.columns else '')

            # Manejo de la fecha de Recordatorio
            if pd.isnull(contacts.loc[contact_index, 'Recordatorio']):
                edited_reminder = st.sidebar.date_input('Recordatorio', datetime.today())
            else:
                edited_reminder = st.sidebar.date_input('Recordatorio', pd.to_datetime(contacts.loc[contact_index, 'Recordatorio']).date())

            if st.sidebar.button('Guardar Cambios'):
                contacts.loc[contact_index, ['Nombre', 'Empresa', 'Correo', 'Teléfono', 'Etiqueta', 'Recordatorio', 'Notas']] = [
                    edited_name, edited_company, edited_email, edited_phone, edited_tag, edited_reminder, edited_note]
                st.write("Contacto actualizado con éxito.")
                st.write(contacts)
        else:
            st.sidebar.write('Selecciona un contacto válido para editar.')
    else:
        st.sidebar.write('No hay contactos para editar.')

# Eliminar Contactos
st.sidebar.header('Eliminar Contacto')
if not contacts.empty:
    contact_to_delete = st.sidebar.selectbox('Selecciona un Contacto para Eliminar', contacts['Nombre'])
    if st.sidebar.button('Eliminar Contacto'):
        contacts = contacts[contacts['Nombre'] != contact_to_delete]
        st.write(f"Contacto {contact_to_delete} eliminado con éxito.")
        st.write(contacts)

# Etiquetado de Contactos
st.sidebar.header('Etiquetado de Contactos')
if not contacts.empty:
    contact_to_tag = st.sidebar.selectbox('Selecciona un Contacto para Etiquetar', contacts['Nombre'])
    tag = st.sidebar.text_input('Etiqueta para Contacto Existente')
    if st.sidebar.button('Añadir Etiqueta'):
        contacts.loc[contacts['Nombre'] == contact_to_tag, 'Etiqueta'] = tag
        st.write(f"Etiqueta '{tag}' añadida a {contact_to_tag}")
        st.write(contacts)

# Recordatorios de Seguimiento
st.sidebar.header('Recordatorios de Seguimiento')
if not contacts.empty:
    contact_to_remind = st.sidebar.selectbox('Selecciona un Contacto para Recordatorio', contacts['Nombre'])
    reminder_date = st.sidebar.date_input('Fecha del Recordatorio para Contacto Existente')
    if st.sidebar.button('Añadir Recordatorio'):
        contacts.loc[contacts['Nombre'] == contact_to_remind, 'Recordatorio'] = reminder_date
        st.write(f"Recordatorio añadido para {contact_to_remind} en la fecha {reminder_date}")
        st.write(contacts)

# Análisis de Interacciones
st.sidebar.header('Análisis de Interacciones')
if not contacts.empty:
    interaction_contact = st.sidebar.selectbox('Selecciona un Contacto para Analizar Interacciones', contacts['Nombre'])
    if st.sidebar.button('Mostrar Análisis'):
        st.write(f"Mostrando interacciones para {interaction_contact}")
        st.write(contacts[contacts['Nombre'] == interaction_contact])

# Exportar Contactos en CSV
st.sidebar.header('Exportar Contactos')
if not contacts.empty:
    if st.sidebar.button('Descargar Contactos en CSV'):
        csv = contacts.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="contactos.csv">Descargar archivo CSV</a>'
        st.sidebar.markdown(href, unsafe_allow_html=True)

# Gráficos y Visualizaciones
st.sidebar.header('Visualizaciones')
if st.sidebar.checkbox('Mostrar Gráfico de Etiquetas'):
    tag_counts = contacts['Etiqueta'].value_counts()
    fig, ax = plt.subplots()
    tag_counts.plot(kind='bar', ax=ax)
    st.pyplot(fig)

# Guardar Cambios
st.sidebar.header('Guardar Cambios')
if st.sidebar.button('Guardar Contactos'):
    contacts.to_csv('contacts_updated.csv', index=False)
    st.sidebar.write("Contactos guardados con éxito")

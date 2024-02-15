import plotly.express as px
import streamlit as st
import pandas as pd
import os
import warnings
import matplotlib
import plotly.figure_factory as ff
warnings.filterwarnings("ignore")

# Encabezado de pestaña de navegador
st.set_page_config(page_title="DASHBORD PBA", page_icon=":hospital:", layout="wide")

#Título y estilo de la página
st.title(":hospital: DASHBOARD DE HOSPITALES PROVINCIA DE BUENOS AIRES")
st.markdown('<style>div.block-container{padding-top:1rem;}<style>', unsafe_allow_html=True)

#Carga de datos
fl=st.file_uploader(":file_folder: Cargar Base de Datos", type=(["csv", "txt", "xlsx", "xls"]))
if fl is not None:
    filename=fl.name
    st.write(filename)
    df = pd.read_csv(filename, delimiter=';', encoding= "ISO-8859-1")
else:
    os.chdir(r"C:\Users\Int18\Desktop\Proyecto Dashbord")
    df = pd.read_csv("Data.csv", delimiter=';', encoding= "ISO-8859-1")

#Definición de columnas de info
col1 , col2  = st.columns((2))

#Campo de fecha de ingreso de Sipach
df["Fecha de Inicio"]= pd.to_datetime(df["txt_fecha_ini"])

#Fechas minimas y máximas de ingreso
startDate = pd.to_datetime(df["Fecha de Inicio"] ).min()

endDate = pd.to_datetime(df["Fecha de Inicio"] ).max()


#Fechas de referencia
with col1:
    date1 = pd.to_datetime(st.date_input("Fecha Inicial", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("Fecha Final", endDate))

#utilización de las fechas maximas y minimas
df = df[(df["Fecha de Inicio"] >= date1) & (df["Fecha de Inicio"] <=date2)].copy()

#Panel Lateral
st.sidebar.header("Eliga los filtros geográficos")

#Selección de Región Sanitaria
region = st.sidebar.multiselect("Elija la Región Sanitaria:", df["txt_regsan"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["txt_regsan"].isin(region)]

#Selección de Municipio
municipio = st.sidebar.multiselect("Elija el Municipio:", df2["txt_muni"].unique())
if not municipio:
    df3 = df2.copy()
else:
    df3 = df2[df2["txt_muni"].isin(municipio)]

#Selección de Hospital
hospital = st.sidebar.multiselect("Elija el Hospital:", df3["combo_hospital"].unique())

#Filtrado de datos en función de Región Sanitaria Municipio y Hospital
if not region and not municipio and not hospital:
    filtered_df = df
elif not municipio and not hospital:
    filtered_df = df[df["txt_regsan"].isin(region)]
elif not region and not hospital:
    filtered_df = df[df["txt_muni"].isin(municipio)]
elif region and municipio:
    filtered_df = df3[df["txt_regsan"].isin(region) & df3["txt_muni"].isin(municipio)]
elif region and hospital:
    filtered_df = df3[df["txt_regsan"].isin(region) & df3["combo_hospital"].isin(hospital)]
elif municipio and  hospital:
    filtered_df = df3[df["txt_muni"].isin(municipio) & df3["combo_hospital"].isin(hospital)]
elif hospital:
    filtered_df = df3[df3["combo_hospital"].isin(hospital)]
else:
    filtered_df = df3[df3["txt_regsan"].isin(region) & df3["txt_muni"].isin(municipio) & df3["combo_hospital"].isin(hospital)]

# Creamos columnas para tipo de intervención
intervencion_df = filtered_df.groupby(by = ["combo_intervencion"], as_index = False)["txt_monto_sol"].sum()

# Creación de chart 1

#Grafico de Barras
with col1:
    st.subheader("Monto de Solicitud por intervención")
    fig = px.bar(intervencion_df, x="combo_intervencion", y="txt_monto_sol",
                 template="seaborn", labels=dict(combo_intervencion="INTERVENCIÓN", txt_monto_sol="MONTO", color="Place"))
    st.plotly_chart(fig,use_container_width=True, height=200)

#Grafico de Torta Monto Solicitud
with col2:
    st.subheader("Monto de Solicitud por Región")
    fig = px.pie(filtered_df, values="txt_monto_sol", names="txt_regsan", hole=0.0)
    fig.update_traces(text=filtered_df["txt_regsan"], textposition = "outside")
    st.plotly_chart(fig, use_container_width=True)


#Creación de botones de descaga de los chart 1
with col1:
    with st.expander("Monto Solicitud por Intervención"):
        st.write(intervencion_df.style.background_gradient(cmap="Blues"))
        csv = intervencion_df.to_csv(index = False).encode('utf-8')
        st.download_button("Descarga datos", data=csv, file_name="IntervenciónSol.csv", mime="text/csv", help="Click para descargar datos")

with col2:
    with st.expander("Monto Solicitud por Región Sanitaria"):
        region = filtered_df.groupby( by = "txt_regsan", as_index = False)["txt_monto_sol"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv = region.to_csv(index = False).encode('utf-8')
        st.download_button("Descarga datos", data=csv, file_name="RegionSanSol.csv", mime="text/csv", help="Click para descargar datos")

# Creamos columnas para tipo de intervención
intervencion_df = filtered_df.groupby(by = ["combo_intervencion"], as_index = False)["txt_monto_pread"].sum()

# Creación de chart 2

#Grafico de Barras
with col1:
    st.subheader("Monto de Preadjudicación por Intervención")
    fig = px.bar(intervencion_df, x="combo_intervencion", y="txt_monto_pread",
                 template="seaborn", labels=dict(combo_intervencion="INTERVENCIÓN", txt_monto_sol="MONTO PREAD", color="Place"))
    st.plotly_chart(fig,use_container_width=True, height=200)

#Grafico de Torta Monto Solicitud
with col2:
    st.subheader("Monto de Preadjudicación por Región")
    fig = px.pie(filtered_df, values="txt_monto_pread", names="txt_regsan", hole=0.0)
    fig.update_traces(text=filtered_df["txt_regsan"], textposition = "outside")
    st.plotly_chart(fig, use_container_width=True)


#Creación de botones de descaga de los chart 2
with col1:
    with st.expander("Monto de Preadjudicación por Intervención"):
        st.write(intervencion_df.style.background_gradient(cmap="Blues"))
        csv = intervencion_df.to_csv(index = False).encode('utf-8')
        st.download_button("Descarga datos", data=csv, file_name="IntervenciónPread.csv", mime="text/csv", help="Click para descargar datos")

with col2:
    with st.expander("Monto de Preadjudicación por Región Sanitaria"):
        region = filtered_df.groupby( by = "txt_regsan", as_index = False)["txt_monto_pread"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv = region.to_csv(index = False).encode('utf-8')
        st.download_button("Descarga datos", data=csv, file_name="RegionSanPread.csv", mime="text/csv", help="Click para descargar datos")


#Linea de tiempo de Inversión Hopitalaria
filtered_df['txt_fecha_oc'] = pd.to_datetime(filtered_df['txt_fecha_oc'])
filtered_df["mes_año"]=filtered_df["txt_fecha_oc"].dt.to_period("M")
st.subheader("Analisis inversión por Tiempo")

#Grafico de linea
linechart = pd.DataFrame(filtered_df.groupby(filtered_df["mes_año"].dt.strftime("%Y : %b"))["txt_monto_pread"].sum()).reset_index()
fig2 = px.line(linechart, x= "mes_año", y="txt_monto_pread", labels={"txt_monto_pread": "MONTO"}, height=500, width=1000, template="gridon")
st.plotly_chart(fig2, use_container_width=True)

#Botón de descarga de grafico de linea
with st.expander("Linea de Tiempo de Inversión Hospitalaria"):
        st.write(linechart.T.style.background_gradient(cmap="Blues"))
        csv = linechart.to_csv(index = False).encode('utf-8')
        st.download_button("Descarga datos", data=csv, file_name="LineadeTiempo.csv", mime="text/csv", help="Click para descargar datos")

#Vision Gerárquica de datos
st.subheader("Visión Jerárquica de Datos")
fig3 = px.treemap(filtered_df, path=["txt_regsan","combo_intervencion", "combo_area", "combo_servicio"], values= "txt_monto_pread", color="combo_servicio")
fig3.update_layout(width = 800, height = 650)
st.plotly_chart(fig3, use_container_width=True)

#Grafico de torta para area y servicio
chart1 , chart2 = st.columns((2))
with chart1:
    st.subheader("Monto por Area")
    fig = px.pie( filtered_df, values="txt_monto_pread", names= "combo_area", template= "plotly_dark")
    fig.update_traces( text=filtered_df["combo_area"], textposition = "inside")
    st.plotly_chart(fig, use_container_width=True)

filtered_df = filtered_df[filtered_df['combo_servicio'] != "NO APLICA"]
with chart2:
    st.subheader("Monto por Servicio")
    fig = px.pie( filtered_df, values="txt_monto_pread", names= "combo_servicio", template= "gridon")
    fig.update_traces( text=filtered_df["combo_servicio"], textposition = "inside")
    st.plotly_chart(fig, use_container_width=True)

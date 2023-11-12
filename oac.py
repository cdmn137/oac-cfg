import streamlit as st
import pandas as pd
import altair as alt


st.write("""
# Comunicaciones*
""")

df = pd.read_excel("casos.xlsx")
df =  df.loc[~df["Transmisor/Nombre"].str.contains("prueba"), ]

# -- Grafico de estatus --
valores = df["Estatus"].value_counts()

source = pd.DataFrame({"category": valores.index, "value": valores})

ch = alt.Chart(source).mark_arc().encode(
    theta="value",
    color="category"
)

st.altair_chart(
    (ch).interactive(),
    use_container_width=True
)


estatus = st.sidebar.selectbox('Seleccione el estatus', [ 'process', 'confirm', 'bound', 'reply', 'waiting', 'unanswered'])
df_process = df.loc[(df["Estatus"]==estatus), ]


responsable = st.sidebar.selectbox('Seleccione el responsable', ['Todos', 'LUIS GERMAN RIVAS ZAMBRANO', 'CRUZ DAVID MATA NOGUERA',
       'CIRO ANTONIO RODRIGUEZ VILLANUEVA',
       'SOFIA MARGARITA FLEURY HERNANDEZ',
       'CESAR EDUARDO CARRERO ARISTIZABAL', 'RICARDO JOSE MUSETT ROMAN',
       'LUISANA VALENTINA VELASQUEZ FERMIN',
       'JOALI GABRIELA MORENO PINTO'])

if (responsable != "Todos"):
    df_process = df_process.loc[(df_process["Responsable/Mostrar nombre"] ==responsable), ]
    

# -- Grafico de categorias --

st.subheader('Casos por Asunto')

categorias = df_process["Categoría/Nombre de categoría"].value_counts()

df_categorias = pd.DataFrame({"categoria":categorias.index, "valores":categorias})

bar = alt.Chart(df_categorias).mark_bar().encode(
    x= alt.X("categoria", sort=None),
    y="valores"
)

st.altair_chart(
    (bar).interactive(),
    use_container_width=True
)



t_min= df_process["Creado en"].min()


st.subheader('El mas urgente de atender')
st.dataframe(df_process.loc[(df_process["Creado en"]==t_min), ])

st.subheader('por atender rapido')
st.dataframe(df_process.sort_values(by=["Creado en"]).head(100))

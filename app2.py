# Importing Libraries
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from streamlit.components.v1 import html
from streamlit_option_menu import option_menu
import warnings
# Importing Our Multipages
import principal
import productos
import ubicaciones


def run():
    st.set_page_config(
        page_title="Tendencias de Compra",
        page_icon="🛍️",
        layout="wide"
    )

    warnings.simplefilter(action='ignore', category=FutureWarning)

    # Function To Load Our Dataset
    @st.cache_data
    def load_data(the_file_path):
        the_file_path=("C:/Users/DELL/Downloads/Dash/español_mod.csv")
        df = pd.read_csv(the_file_path)
        return df

    df = load_data("español_mod.csv")

    st.markdown(
        """
    <style>
         .main {
            text-align: center; 
         }

         div.block-containers{
            padding-top: 0.5rem
         }

         .st-emotion-cache-z5fcl4{
            padding-top: 1rem;
            padding-bottom: 1rem;
            padding-left: 1.5rem;
            padding-right: 2.8rem;
            overflow-x: hidden;
         }

         .st-emotion-cache-16txtl3{
            padding: 2.7rem 0.6rem
         }
         div.st-emotion-cache-1r6slb0{
            padding: 15px 5px;
            background-color: #111;  
            border-radius: 5px;
            border: 3px solid #A8F0FB;
            opacity: 0.9;
         }
        div.st-emotion-cache-1r6slb0:hover{
            transition: all 0.5s ease-in-out;
            background-color: #2A2A2A;  
            border: 3px solid #06B0FA;
            opacity: 1;
         }

         .plot-container.plotly{
            border: 4px solid #06B0FA;
            border-radius: 7px;
         }

         div.st-emotion-cache-1r6slb0 span.st-emotion-cache-10trblm{
            font: bold 24px tahoma
         }
         div [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
        
        .stMultiSelect [data-baseweb="tag"] {
        background-color: #06B0FA !important; /* Color del fondo del recuadro de las etiquetas seleccionadas */
        color: white !important; /* Color del texto de las etiquetas seleccionadas */
        
        }


    </style>
    """,
        unsafe_allow_html=True
    )

    header = st.container()
    content = st.container()

    with st.sidebar:
        page = option_menu(
            menu_title='Menu',
            options=['Principal', 'Productos', "Ubicaciones"],
            icons=['house-fill', 'person-circle', "map-fill"],
            menu_icon='menu-app-fill',
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": '#001456'},
                "icon": {"color": "white", "font-size": "20px"},
                "nav-link": {"color": "#D2EBFB", "font-size": "18px", "text-align": "left", "margin": "0px", },
                "nav-link-selected": {"background-color": "#06B0FA"},
                "menu-title": {"color": "#D2EBFB", "font-size": "25px", "font-weight": "bold"},

            }

        )

        st.write("***")

        # Get All Locations as a list
        location_options = sorted(df["Ubicación"].unique().tolist())
        location_options.insert(0, "ALL")

        # Home Page
        if page == "Principal":
            category_filter = st.multiselect("Selecciona Categoría 👕💎:athletic_shoe:",
                                             options=sorted(
                                                 df["Categoría"].unique().tolist()),
                                             default=sorted(
                                                 df["Categoría"].unique().tolist()))

            size_filter = st.multiselect("Selecciona Talla 👔",
                                         options=sorted(
                                             df["Tamaño"].unique().tolist()),
                                         default=sorted(
                                             df["Tamaño"].unique().tolist()))

            location_filter = st.selectbox("Selecciona Ubicación 🌏",
                                           options=location_options,
                                           index=0)

            with header:
                principal.home_header()

            with content:
                df_filtered = principal.filter_data(df, category_filter,
                                               size_filter, location_filter)

                left_col, mid_col, right_col = st.columns(3)

                with left_col:
                    st.subheader("Total Clientes")
                    st.subheader(principal.total_customers(df_filtered))

                with mid_col:
                    st.subheader("Califiación Promedio")
                    st.subheader(principal.avergae_rating(df_filtered))

                with right_col:
                    st.subheader("Total Compras")
                    st.subheader(principal.total_purchases(df_filtered))

                st.markdown("---")

                left_chart, right_chart = st.columns(2)
                with left_chart:
                    st.plotly_chart(principal.create_category_chart(
                        df_filtered), use_container_width=True)

                with right_chart:
                    st.plotly_chart(principal.create_gender_chart(
                        df_filtered), use_container_width=True)

                st.markdown("---")
                st.plotly_chart(principal.create_shipping_chart(
                    df_filtered), use_container_width=True)

        # Products Page
        if page == "Productos":
            category_filter = st.multiselect("Selecciona Categoría 👕💎:athletic_shoe:",
                                             options=sorted(
                                                 df["Categoría"].unique().tolist()),
                                             default=sorted(
                                                 df["Categoría"].unique().tolist()))

            size_filter = st.multiselect("Selecciona Talla 👔",
                                         options=sorted(
                                             df["Tamaño"].unique().tolist()),
                                         default=sorted(
                                             df["Tamaño"].unique().tolist()))

            location_filter = st.selectbox("Selecciona Ubicación 🌏",
                                           options=location_options,
                                           index=0)
            with header:
                productos.products_header()

            with content:
                df_filtered = productos.filter_data(df, category_filter,
                                                   size_filter, location_filter)

                left_col, mid_col, right_col = st.columns(3)

                with left_col:
                    st.image("C:/Users/DELL/Downloads/Dash/imgs/dollar.png", caption="", width=70)
                    st.subheader("Total de Ventas")
                    st.subheader(productos.total_sales(df_filtered))

                with mid_col:
                    st.image("C:/Users/DELL/Downloads/Dash/imgs/clothes.png", width=70)
                    st.subheader("Categorias")
                    st.subheader(productos.number_of_category(df))

                with right_col:
                    st.image("C:/Users/DELL/Downloads/Dash/imgs/online-shopping.png", width=70)
                    st.subheader("Productos")
                    st.subheader(productos.number_of_products(df_filtered))
                st.markdown("---")

                products_left_chart, products_right_chart = st.columns([7, 5])

                with products_left_chart:
                    st.plotly_chart(productos.create_products_chart(df_filtered),
                                    use_container_width=True)

                with products_right_chart:
                    st.plotly_chart(productos.create_size_chart(
                        df_filtered), use_container_width=True)

                st.plotly_chart(
                    productos.category_via_season_chart(df_filtered),
                    use_container_width=True)

        # Locations Page
        if page == "Ubicaciones":

            category_filter = st.multiselect("Selecciona Categoría 👕💎:athletic_shoe:",
                                             options=sorted(
                                                 df["Categoría"].unique().tolist()),
                                             default=sorted(
                                                 df["Categoría"].unique().tolist()))

            size_filter = st.multiselect("Selecciona Talla 👔",
                                         options=sorted(
                                             df["Tamaño"].unique().tolist()),
                                         default=sorted(
                                             df["Tamaño"].unique().tolist()))

            season_filter = st.multiselect("Selecciona Temporada :snowflake::sunny::rain_cloud::fallen_leaf:",
                                           options=sorted(
                                               df["Temporada"].unique().tolist()),
                                           default=sorted(
                                               df["Temporada"].unique().tolist()))
            with header:
                ubicaciones.sales_header()

            with content:
                df_filtered = ubicaciones.filter_data(df, category_filter,
                                                    size_filter, season_filter)

                st.plotly_chart(ubicaciones.create_map(df_filtered),
                                use_container_width=True)

                st.markdown("---")

                st.plotly_chart(ubicaciones.create_subscription_via_location(df_filtered),
                                use_container_width=True)

                st.markdown("---")

                l_c, r_c = st.columns([7, 5])
                with l_c:

                    st.plotly_chart(ubicaciones.create_location_category(df_filtered),
                                    use_container_width=True)

                with r_c:
                    st.plotly_chart(ubicaciones.create_top3_review(
                        df_filtered), use_container_width=True)


run()
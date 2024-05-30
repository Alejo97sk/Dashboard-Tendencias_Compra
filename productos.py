# Importing Libraries
import plotly.express as px
import streamlit as st

def products_header():
    st.title("Productos :shopping_bags:")

def filter_data(df, category_filter, size_filter, location_filter):
    filt = (df["Categoría"].isin(category_filter)) & (df["Tamaño"].isin(size_filter))
    if location_filter != "ALL":
        filt &= (df["Ubicación"] == location_filter)
    return df[filt]

def number_of_products(the_df):
    return the_df["Artículo_Comprado"].nunique()

def number_of_category(the_df):
    return the_df["Categoría"].nunique()

def total_sales(the_df):
    return f'{the_df["Precio_USD"].sum():,.0f}'

def create_products_chart(the_df):
    top_5_products = the_df["Artículo_Comprado"].value_counts().nlargest(5)
    fig = px.bar(top_5_products,
                 x=top_5_products.values,
                 y=top_5_products.index,
                 orientation="h",
                 color=top_5_products.index,
                 color_discrete_sequence=["#81C0FF","#B581FF","#81FFDB","#81FF85","#D478EB"],
                 labels={"x": "Frecuencia de Artículos Vendidos", "y": "Artículo"},
                 text_auto=True,
                 title="Top 5 Artículos Vendidos"
    )
    fig.update_layout(
        showlegend=False,
        title={"font": {"size": 20, "family": "tahoma"}, "x": 0.5, "xanchor": "center"},
        hoverlabel={"bgcolor": "#222", "font_size": 15, "font_family": "tahoma"},
        yaxis={"title": 'Artículo Comprado', "tickfont": {"size": 15}, "title_font": {"size": 18}},
        xaxis={"title": 'Frecuencia', "tickfont": {"size": 15}, "title_font": {"size": 18}}
    )
    fig.update_traces(
       textfont={"family": "consolas", "size": 17, "color": "#fff"},
       hovertemplate="Producto: %{x}<br>Popularidad (%): %{y:.1f}%"
    )
    return fig

def create_size_chart(the_df):
    the_df = the_df.dropna(subset=["Tamaño", "Género"])  # Asegurarse de que no haya valores nulos en "Tamaño" y "Género"
    size_by_gender = the_df.pivot_table(index="Género", columns="Tamaño", values="Artículo_Comprado", aggfunc="count", fill_value=0)
    size_by_gender = size_by_gender.stack().reset_index(name="Count")
    custom_palette = ['#1AAFE3', '#8E21FB']
    fig = px.sunburst(size_by_gender,
                      path=['Género', 'Tamaño'],
                      values='Count',
                      color_discrete_sequence=custom_palette,
                      title="Frecuencia de Tamaño por Género",
    )

    fig.update_layout(
        title={"font": {"size": 20, "family": "tahoma"}, "x": 0.5, "xanchor": 'center'},
        hoverlabel={"bgcolor": "black", "font_size": 15, "font_family": "tahoma"}
    )

    fig.update_traces(
        textinfo='label+percent entry',
        textfont={"family": "tahoma", "size": 15, "color": 'white'},
        hovertemplate="Género: %{label}<br>Frecuencia: %{value:.0f}"
    )
    return fig

def category_via_season_chart(the_df):
    sales_per_category = the_df.groupby("Categoría")["Precio_USD"].sum().sort_values(ascending=False)
    fig = px.bar(sales_per_category,
         x = sales_per_category.index,
         y = sales_per_category,
         labels = {"y" : "Ventas_USD"},
         text_auto="0.4s",
         title = "Ventas en USD por Categoría",
         color = sales_per_category.index,
         color_discrete_sequence=['#565DA8', '#56A865', '#A28FB7', '#aec7e8']
    )

    fig.update_layout(
        showlegend=False,
        xaxis={"title": 'Categoría', "tickfont": {"size": 15, "family": 'Arial'}, "title_font": {"size": 20}},
        yaxis={"title": 'Ventas (USD)', "tickfont": {"size": 15, "family": 'Arial'}, "title_font": {"size": 20}},
        title={"font": {"size": 25, "family": "Arial"}, "x": 0.5, "xanchor": 'center'}
    )
    fig.update_traces(
        textfont={"family": "tahoma", "size": 16, "color": "#fff"},
        hovertemplate="Categoría:%{x}<br>Ventas USD: %{y}"
    )
    return fig

import pandas as pd
import plotly.express as px
import streamlit as st

def sales_header():
    st.title('Ubicaciones :globe_with_meridians:')

def filter_data(df, category_filter, size_filter, season_filter):

    filt = (df["Categoría"].isin(category_filter)) &\
        (df["Tamaño"].isin(size_filter)) &\
        (df["Temporada"].isin(season_filter))

    return df[filt]

# Function To Get The latitude and longitude for each Location
@st.cache_data
def load__locations_data():
    positions = pd.read_csv(
        "https://raw.githubusercontent.com/jasperdebie/VisInfo/master/us-state-capitals.csv")

    return positions

def create_map(the_df):
    pos = load__locations_data()
    alt_df = the_df.merge(pos, left_on="Ubicación", right_on="name", how="left") \
                  .groupby(["Ubicación", "latitude", "longitude"], as_index=False)["Precio_USD"].sum()

    fig = px.scatter_mapbox(alt_df, lat="latitude", lon="longitude", hover_name="Ubicación",
                            hover_data=["Precio_USD"], color="Precio_USD", size="Precio_USD",
                            color_continuous_scale=px.colors.cyclical.Twilight, zoom=3, height=650,
                            title="Ubicaciones y sus precios de venta"
    )
    fig.update_layout(
        mapbox_style="open-street-map",
        title={"text": "Ubicaciones y sus precios de venta", "font":{"size": 25, "family": "tahoma"}, "x": 0.5, "xanchor": "center"},
        hoverlabel={"bgcolor": "#222", "font_size": 15, "font_family": "tahoma"}
    )
    return fig

def get_top_n(the_df, n):
    top_n_location = the_df.groupby("Ubicación")["Precio_USD"]\
        .sum().nlargest(n)
    top_n_location = top_n_location.index.tolist()

    filt = the_df["Ubicación"].isin(top_n_location)
    return the_df[filt]

def create_subscription_via_location(the_df):
    purchases_by_loc = the_df.groupby("Ubicación")["Compras_Anteriores"].sum().nlargest(10)
    fig = px.bar(purchases_by_loc, orientation="h", text_auto="0.4s", labels={"x": "Total Compras"},
                 title="Top 10 Número de compras por Estado", color_discrete_sequence=["#8DBBDF"], template="plotly_dark"
    )
    fig.update_layout(
        showlegend=False,
        title={"text": "Top 10 Número de compras por Estado","font":{ "size": 25, "family": "tahoma"}, "x": 0.5, "xanchor": "center"},
        xaxis=dict(title='Total Compras', title_font=dict(size=18)),
        yaxis=dict(title='Ubicación', title_font=dict(size=18))
    )
    fig.update_traces(
        textfont={"family": "tahoma", "size": 14, "color": "#fff"},
        hovertemplate="State: %{y}<br>Total Purchases: %{x:0.4s}"
    )
    return fig

def create_location_category(the_df):
    dff = get_top_n(the_df, 5)
    category_via_loc = dff.groupby("Ubicación", as_index=False)["Categoría"]\
    .value_counts()

    fig = px.sunburst(category_via_loc, path=['Ubicación', 'Categoría'], values='count',
                      color_discrete_sequence=["#B403C2", "#7703C2", "#0329C2", "#03AEC2", "#03C251"],
                      title="Top 5 estados y su popularidad de categorías"
    )
    fig.update_layout(
        title={"text": "Top 5 estados y su popularidad de categorías","font":{ "size": 20, "family": "tahoma"}, "x": 0.5, "xanchor": "center"},
        hoverlabel={"bgcolor": "#222", "font_size": 14, "font_family": "tahoma"}  
    )
    fig.update_traces(
        textfont={"family": "tahoma", "size": 13}, 
        hovertemplate="%{label}<br>Popularidad (%): %{value:.0f}%"
    )
    return fig

def create_top3_review(the_df):
    loc_review = the_df.groupby("Ubicación")["Calificación_de_Reseña"].mean().nlargest(3)
    fig = px.bar(loc_review, color_discrete_sequence=["#049FE8"], template="plotly_dark", text_auto="0.1f",
                 labels={"value": "PROM Calficación", "Estado_de_Suscripción": "Estado_de_Suscripción"},
                 title="Los 3 estados con mejor valoración"
    )
    fig.update_layout(
        showlegend=False,
        title={"text": "Los 3 estados con mejor valoración", "font":{"size": 20, "family": "tahoma"}, "x": 0.5, "xanchor": "center"},
        xaxis=dict(title='Ubicación', title_font=dict(size=18)),
        yaxis=dict(title='PROM Calificación', title_font=dict(size=18))
    )
    fig.update_traces(
        textfont={"family": "tahoma", "size": 15}, 
        hovertemplate="State: %{x}<br>AVG Review: %{y:.1f}"
    )
    return fig

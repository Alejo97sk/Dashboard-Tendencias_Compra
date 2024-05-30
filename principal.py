import pandas as pd
import plotly.figure_factory as ff
import plotly.express as px
import streamlit as st

def home_header():
    st.title('Panel de Tendencias de Compra :chart_with_upwards_trend:')

def filter_data(df, category_filter, size_filter, location_filter):
    if location_filter == "ALL":
        filt = (df["Categoría"].isin(category_filter)) &\
            (df["Tamaño"].isin(size_filter))
    else:
        filt = (df["Categoría"].isin(category_filter)) &\
            (df["Tamaño"].isin(size_filter)) &\
            (df["Ubicación"] == location_filter)
    return df[filt]

def total_customers(the_df):
    return f"{len(the_df):,.0f}"

def avergae_rating(the_df):
    return round(the_df["Calificación_de_Reseña"].mean(), 1)

def total_purchases(the_df):
    return f"{the_df['Compras_Anteriores'].sum():,.0f}"

def create_category_chart(the_df):
    category_per_season = the_df.pivot_table(index = "Temporada", columns = the_df["Categoría"], values ="Categoría", aggfunc="count")
    total = category_per_season[category_per_season.columns].sum(1)
    category_per_season.loc["Otoño"]  = round(category_per_season.loc["Otoño"] / total.values[0] * 100)
    category_per_season.loc["Primavera"] = round(category_per_season.loc["Primavera"] / total.values[1] * 100)
    category_per_season.loc["Verano"] = round(category_per_season.loc["Verano"] / total.values[2] * 100)
    category_per_season.loc["Invierno"] = round(category_per_season.loc["Invierno"] / total.values[3] * 100)
    fig = px.bar(category_per_season, barmode="group", x = category_per_season.index, y = category_per_season.columns,
                 color_discrete_sequence=["#2F62CE","#4C98EC","#0B02C3","#75D2FD"], text_auto="%0.0f",
                 title="Popularidad en % de Categoría por Temporada", labels={"value" : "Popularidad (%)","index":"Temporada"},
     )
    fig.update_layout(
        title={"font": {"size": 20, "family": "tahoma"}, "x": 0.5, "xanchor": 'center'},
        xaxis={"title": 'Temporada', "tickfont": {"size": 15, "family": 'tahoma'}, "title_font": {"size": 18}},
        yaxis={"title": 'Popularidad (%)', "tickfont": {"size": 15, "family": 'tahoma'}, "title_font": {"size": 18}},
    )
    fig.update_traces(
        textfont={"family": "tahoma", "size": 11, "color": "#fff"},
        hovertemplate="%{label}<br>Popularidad (%): %{y}%"
    )
    return fig

def create_gender_chart(the_df):
    discount_by_status = pd.crosstab(index = the_df["Estado_de_Suscripción"], 
                                columns=the_df["Descuento_Aplicado"], 
                                values=the_df["Descuento_Aplicado"], 
                                 aggfunc="count", normalize=0) * 100

    fig = px.bar(discount_by_status, text_auto=".1f", title="Descuento aplicado por cada suscripción",
                 color_discrete_sequence=["#6F04E8", "#04E82A"], template="plotly_dark",
                 labels={"Estado_de_Suscripción": "Estado de Suscripción", "value": "Porcentaje (%)"}
        )
    fig.update_layout(
     title={"font": {"size": 20, "family": "tahoma"}, "x": 0.5, "xanchor": "center"},
        xaxis={"title": 'Estado de suscripción', "tickfont": {"size": 15}, "title_font": {"size": 18}},
        yaxis={"title": 'Porcentaje (%)', "tickfont": {"size": 15}, "title_font": {"size": 18}},
        legend_title_text='Descuento Aplicado',    
        )
    fig.update_traces(
        textfont={"family": "tahoma", "size": 16, "color": "white"},
        hovertemplate="Subscription Status: %{x}<br>Total Purchases: %{value:.4s}",
        )
    return fig

def create_shipping_chart(the_df):
    hist_data = [the_df['Edad'].dropna()]
    group_labels = ['Edades']
    fig = ff.create_distplot(hist_data, group_labels, bin_size=5, curve_type='kde',
                            show_hist=True, show_rug=False, colors=['#26DB2B'])
    mean_age = the_df['Edad'].mean()
    fig.add_vline(x=mean_age, line=dict(color='#8000FF', dash='dash'), 
                 annotation_text=f'Edad Promedio ({mean_age:.0f})', annotation_position='top left')
    fig.update_layout(
        title={"text": 'Distribución de Edades con Curva de Densidad', "font": {"size": 25}, "x": 0.5, "xanchor": 'center'},
        xaxis={"title": 'Edad', "title_font": {"size": 18}},
        yaxis={"title": 'Densidad', "title_font": {"size": 18}},
        showlegend=False,   
    )
    return fig

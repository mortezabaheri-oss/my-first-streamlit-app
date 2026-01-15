# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 14:03:20 2026

@author: morte
"""
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

st.set_page_config(page_title="population in top 20 country", page_icon=":earth_asia:", layout="wide")
st.title(":earth_asia: population in top 20 country for 50 years")

data = pd.read_csv('population_growth.csv')

input_year= data['year']

st.sidebar.header("Filter Data by year: ")

input_year = st.sidebar.selectbox("Select year:",
                                            input_year,
                                            index=0)

data2 = data[data['year'] == input_year]

#fig1
total_pop = data.groupby('year')['population'].sum().to_frame().reset_index()

fig = px.line(total_pop, x = 'year',  y = 'population',title='Top 20 country Population Over Time (1960-2009)',
              labels={'population':'Population (millions)'})
st.plotly_chart(fig, use_container_width=True)

#fig2
top_growth = data2.groupby(['country','year'])['population_growth_rate'].mean().reset_index()
fig = px.bar(top_growth, 
             x='country', y='population_growth_rate',
             title=f'Top Countries by Population Growth Rate in {input_year}',
             width = 700, height= 800,
             labels={'population_growth_rate':'population growth rate'})
fig.update_layout(
    xaxis={'categoryorder':'total descending'})
st.plotly_chart(fig, use_container_width=True )

#make col
col1,col2=st.columns((2))

#fig3
with col1:
    fig = px.scatter(data, x='fertility_rate', y='population_growth_rate',
                  size='population', color='continent', hover_name='country',
                  animation_frame='year', title='Fertility Rate vs Growth Rate by year',
                  opacity=0.8,size_max=50,
                  range_x=[0, 3.6],
                  labels={'fertility_rate':'Fertility Rate', 'population_growth_rate':'Growth Rate (%)'})
        
           
    st.plotly_chart(fig, use_container_width=True)  
 
    
#fig4
with col2:
    income_urban = data.groupby(['income_group', 'year'])['urban_population'].mean().reset_index()
    
    fig = px.line(income_urban, x='year', y='urban_population', color='income_group',
              title='Urban Population Share by Income Group Over Time',
             labels={'urban_population':'urban_population_share(%)'})
    st.plotly_chart(fig, use_container_width=True)  
    
    
#fig5
continent_age = data.groupby(['continent', 'year'])['median_age'].mean().reset_index()

fig = px.line(continent_age, x='year', y='median_age', color='continent',
              title='Median Age Trends by Continent')
st.plotly_chart(fig, use_container_width=True)  

#fig6 

continent_decade_growth = data.groupby(['continent', 'year'])['population_growth_rate'].mean().reset_index()

fig = px.density_heatmap(continent_decade_growth, x='continent', y='year', 
                         z='population_growth_rate',
                         color_continuous_scale='Reds',
                         title='Avg Population Growth Rate by Continent and Decade')
st.plotly_chart(fig, use_container_width=True)

#fig7
data['decade'] = (data['year'] // 10) * 10
data1 = data.groupby(['continent','country','decade'])[['median_age','fertility_rate']].mean().reset_index()

fig = px.scatter(data1, x='median_age', y='fertility_rate', color='continent',
                 trendline='ols', hover_name='country',
                 title='Median Age vs Fertility Rate in decades (With Trendlines)')
st.plotly_chart(fig, use_container_width=True)

#fig8
data2 = data[data['year'] == input_year]
data2['log_population_density'] = np.log10(data2['population_density'])

fig = px.choropleth(locations=data2['country'], 
                    locationmode="country names", 
                    color=data2['log_population_density'],
                    width=1000,  
                    height=600,  
                    color_continuous_scale='Reds',
                    fitbounds='locations',
                    labels={"color": "population density"},
                    title=f'population density in {input_year}'
                   )
st.plotly_chart(fig, use_container_width=True)
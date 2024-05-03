import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
pd.set_option('display.max_columns', None)
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import requests
from forex_python.converter import CurrencyRates


#streamli part

st.set_page_config(layout= "wide")
st.title("Zomato Data Analysis")
st.write()

def datafr():
    df = pd.read_csv("C:/Users/L/Desktop/Zomato_analysis/zomato.csv")
    return df

df= datafr()

with st.sidebar:
     select= option_menu("Main Menu",["Home", "Data Exploration","Exchange_rates"])


if select == "Home":
     
       st.header("About Zomato : ")

       st.write("Zomato is a popular online food delivery and restaurant discovery platform. It was founded in 2008 by Deepinder Goyal and Pankaj Chaddah. Zomato allows users to search for restaurants, view menus, read reviews, and order food for delivery or pickup.") 
       
       st.write("")
       st.write("")


       st.subheader("Key Information :")

       st.write(''' CEO: Deepinder Goyal
                    Founding Year: 2008
                    Number of Users: Over 150 million monthly active users worldwide
                    Net Worth: Zomato's valuation is estimated to be several billion dollars''')
       
       st.write("")
       st.write("")
       
       

       st.write(''' Now we will  Explore our Zomato analysis to gain insights into restaurant data, cuisines, delivery services, and more''')
                                            


if select =="Data Exploration":     
      
    questions = st.selectbox("select your question",("choose a question",
                                                       "1. Top 5 Cities by Count of Restaurants",
                                                       "2. Count of Restaurants Offering Online Delivery",
                                                       "3. Top 10 Costly Cuisines in India",
                                                       "4. The most common cuisine in each city",
                                                       "5. Top 10 Average Cost for Two for Each Cuisine",
                                                       "6. Rating Count in Top 5 Cities",
                                                       "7. Online Delivery vs. Dine-In",
                                                       "8. Top 10 Cities by Online Delivery Spending in India",
                                                       "9. Total Dine-in Expenditure by City in India",
                                                      "10. Top 10 Cities by Average Cost for Two"))
      
    if questions == "1. Top 5 Cities by Count of Restaurants":
            
          # Bar chart for count of restaurants in each city

        city_counts = df["City"].value_counts().reset_index()
        city_counts.columns = ['City', 'Count'] 
        city_counts = city_counts.sort_values(by='Count', ascending=False)                                            

        # Select top 10 cities 
        top_10_cities = city_counts.head(5)

        # Plot bar chart with different colors for each bars
        fig1 = px.bar(top_10_cities, x='City', y ='Count', title="Top 5 Cities by Count of Restaurants", color ='City')
        st.plotly_chart(fig1)

    elif questions == "2. Count of Restaurants Offering Online Delivery":

          # Bar chart for count of restaurants offering online delivery

        delivery_counts = df["Has Online delivery"].value_counts().reset_index()
        delivery_counts.columns = ['Has Online delivery', 'Count']
        
        fig2 = px.bar(delivery_counts, x='Has Online delivery', y='Count', title='Count of Restaurants Offering Online Delivery', color_discrete_sequence=px.colors.sequential.Redor_r, width=600, height=500) 
        st.plotly_chart(fig2)

    elif questions == "3. Top 10 Costly Cuisines in India":

        indian_restaurants = df[df['Country'] =='India']

        # Calculate average cost for each cuisine
        cuisine_avg_cost = indian_restaurants.groupby('Cuisines')['Average Cost for two'].mean().reset_index()
        cuisine_avg_cost = cuisine_avg_cost.sort_values(by='Average Cost for two', ascending=False)
        
        fig3 = px.bar(cuisine_avg_cost.head(10), x='Cuisines', y='Average Cost for two', 
                    title='Top 10 Costly Cuisines in India', color='Cuisines',color_discrete_sequence=px.colors.sequential.Rainbow_r, width= 600, height= 500)
         
        st.plotly_chart(fig3)

    elif questions == "4. The most common cuisine in each city":
         
        df_cuisines = df['Cuisines'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).rename('Cuisine')
        df_split = df.join(df_cuisines)  

         # Group by city and cuisine, count the occurrences of each cuisine in each city
        city_cuisine_count = df_split.groupby(['City', 'Cuisine']).size().reset_index(name='Count')  

        city_top_cuisine = city_cuisine_count.sort_values(by=['City', 'Count'], ascending=[True, False]).groupby('City').first().reset_index()       
          
        fig4 = px.bar(city_top_cuisine, x='Cuisine', y='Count', 
              title='The most common cuisine in each city', 
              color='Cuisine', 
              color_discrete_sequence=px.colors.sequential.Rainbow_r, 
              width=600, height=500) 
        
        st.plotly_chart(fig4)

    elif questions == "5. Top 10 Average Cost for Two for Each Cuisine":
             
        cuisine_avg_cost = df.groupby('Cuisines')['Average Cost for two'].mean().reset_index()
        cuisine_avg_cost = cuisine_avg_cost.sort_values(by='Average Cost for two', ascending=False).head(10)

        fig5 = px.pie(cuisine_avg_cost, values='Average Cost for two', names='Cuisines', hover_data=["Average Cost for two"],
                       color_discrete_sequence=px.colors.sequential.BuPu_r, title='top 10 Average Cost for Two for Each Cuisine')
     
        st.plotly_chart(fig5)

    elif questions == "6. Rating Count in Top 5 Cities":

          # Filter out the top 5 cities
        top_cities = df['City'].value_counts().head(5).index.tolist()

         #Filter the dataframe for the top 5 cities
        top_cities_df = df[df['City'].isin(top_cities)]

        rating_counts = top_cities_df.groupby(['City', 'Rating text']).size().reset_index(name='Count')
        
        fig6 = px.bar(rating_counts, x='City', y='Count', color='Rating text', 
                facet_col='Rating text', title='Rating Count in Top 5 Cities',
                category_orders={'Rating text': ['Excellent', 'Very Good', 'Good', 'Average', 'Not rated']})
    
        st.plotly_chart(fig6)  

    elif questions == "7. Online Delivery vs. Dine-In":

        delivery_counts = df['Has Online delivery'].value_counts().reset_index()

        delivery_counts.columns = ['Has Online delivery', 'Count']
         
        fig7 = px.pie(delivery_counts, values='Count', names='Has Online delivery', hover_data=["Count"],
                       color_discrete_sequence=px.colors.qualitative.Set3, title='Online Delivery vs. Dine-In')
 
        
        st.plotly_chart(fig7)

    elif questions == "8. Top 10 Cities by Online Delivery Spending in India":
         
        df_india = df[(df['Country'] == 'India') & (df['Has Online delivery'] == 'Yes')]
        
        city_spending = df_india.groupby('City')['Average Cost for two'].sum().reset_index()
        city_spending = city_spending.sort_values(by='Average Cost for two', ascending=False)

         # Slice the DataFrame to select top 10 cities
        top_10_cities = city_spending.head(10)  

        # Plotting the bar chart
        fig8 = px.bar(top_10_cities, x='City', y='Average Cost for two', title='Top 10 Cities by Online Delivery Spending in India', color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig8) 

    elif questions == "9. Total Dine-in Expenditure by City in India":
         
         df_Dine_in= df[(df['Country'] == 'India') & (df['Has Online delivery'] == 'No')]

         city_Dine_in=df_Dine_in.groupby('City')['Average Cost for two'].sum().reset_index()
         city_Dine_in=city_Dine_in.sort_values(by='Average Cost for two', ascending=False)

         top_10 =city_Dine_in.head(10)

         fig9 = px.bar(top_10, x='City', y='Average Cost for two', title='Total Dine-in Expenditure by City in India', color_discrete_sequence=px.colors.sequential.BuPu_r)
         st.plotly_chart(fig9)
    
    elif questions == "10. Top 10 Cities by Average Cost for Two":

         city_avg_cost = df.groupby('City')['Average Cost for two'].mean().reset_index()
         city_avg_cost =city_avg_cost.sort_values(by='Average Cost for two', ascending=False)

         top_10_cities = city_avg_cost.head(10)

         fig10 = px.bar(top_10_cities, x='City', y='Average Cost for two', 
                    title='Top 10 Cities by Average Cost for Two',
                    color_discrete_sequence=px.colors.qualitative.Bold)
    
         st.plotly_chart(fig10) 


if  select == "Exchange_rates":

   

    def fetch_exchange_rates(api_key):

        country_codes = [1, 14, 30, 37, 94, 148, 162, 166, 184, 189, 191, 208, 214, 215, 216]
        # API endpoint for Open Exchange Rates
        api_url = f'https://open.er-api.com/v6/latest?symbols={",".join(map(str, country_codes))}'
  # INR is the base currency

        # Make a request to the API
        response = requests.get(api_url, params={'app_id': api_key})

        # Check if the request was successful
        if response.status_code == 200:
                exchange_data = response.json()
                # Extract exchange rates for different currencies
                exchange_rates = exchange_data['rates']
                return exchange_rates
        else:
                st.error('Failed to fetch exchange rate data')
                return None

    st.title('Real Exchange Rate Comparison')

# Sidebar for API key input
    api_key = st.sidebar.text_input('Enter your Open Exchange Rates API Key')
         
    if api_key:
            exchange_rates = fetch_exchange_rates(api_key) 
            if exchange_rates:
                #Display exchange_rates
                #st.write('Exchange Rates:')
                #st.write(exchange_rates)

                # Calculate the difference between exchange rates and INR
                df_diff = pd.DataFrame(exchange_rates.items(), columns=['Country', 'Exchange Rate'])
                df_diff['Difference'] = df_diff['Exchange Rate'] - 1

            # Plotting the bar chart
                fig = px.bar(df_diff, x='Country', y='Difference',
                         title='Difference in Exchange Rate from Indian Currency (INR)',
                         color='Country', color_discrete_sequence=px.colors.qualitative.Bold)
            # Display the plot using Streamlit
                st.plotly_chart(fig)

                # Your visualization code using exchange_rates goes here
                
            else:
                st.write('Please provide a valid API key')
    else:
        st.write('Please enter your Open Exchange Rates API key in the sidebar')   
 
 
 

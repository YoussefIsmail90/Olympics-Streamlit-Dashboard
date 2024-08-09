import streamlit as st
import pandas as pd
import plotly.express as px

# Title of the app
st.title('Olympics Data Dashboard (1994-2024)')

# Load data
@st.cache_data
def load_data():
    # Replace 'path_to_your_csv.csv' with the actual path to your CSV file
    return pd.read_csv('YoussefIsmail90/Olympics-Streamlit-Dashboard/blob/main/olympics_data.csv')

data = load_data()

# Convert 'Year' to integer
data['Year'] = data['Year'].astype(int)

# Sidebar for interactive filters
st.sidebar.header('Filter Options')

# Filter by NOC (National Olympic Committee)
selected_noc = st.sidebar.selectbox('Select NOC:', sorted(data['NOC'].unique()))

# Filter by year range
year_range = st.sidebar.slider('Select Year Range:', 
                               int(data['Year'].min()), int(data['Year'].max()), 
                               (int(data['Year'].min()), int(data['Year'].max())))

# Apply filters
filtered_data = data[(data['NOC'] == selected_noc) & 
                     (data['Year'] >= year_range[0]) & 
                     (data['Year'] <= year_range[1])]

# Display filtered data as a graph
st.subheader(f'Data for {selected_noc} from {year_range[0]} to {year_range[1]}')

if not filtered_data.empty:
    # Create a DataFrame for plotting
    df_filtered = filtered_data.groupby('Year').sum().reset_index()
    
    fig_line = px.line(df_filtered, x='Year', y=['Gold', 'Silver', 'Bronze'],
                        title=f'{selected_noc} Medal Count Over Time',
                        labels={'value': 'Number of Medals', 'variable': 'Medal Type'},
                        markers=True)
    fig_line.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title='Year', title_font=dict(size=12), tickfont=dict(size=10)),
        yaxis=dict(title='Number of Medals', title_font=dict(size=12), tickfont=dict(size=10)),
        title_font=dict(size=14),
        legend=dict(x=0.8, y=1.1, orientation='h')
    )
    st.plotly_chart(fig_line)

    st.subheader('Medal Count Over the Years')
    df_medals = filtered_data[['Year', 'Gold', 'Silver', 'Bronze']].groupby('Year').sum().reset_index()
    fig_bar = px.bar(df_medals, x='Year', y=['Gold', 'Silver', 'Bronze'],
                     title=f'{selected_noc} Medal Count Over Time',
                     labels={'value': 'Number of Medals', 'variable': 'Medal Type'},
                     height=300,
                     color_discrete_map={'Gold': 'gold', 'Silver': 'silver', 'Bronze': '#cd7f32'})
    fig_bar.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title='Year', title_font=dict(size=12), tickfont=dict(size=10)),
        yaxis=dict(title='Number of Medals', title_font=dict(size=12), tickfont=dict(size=10)),
        title_font=dict(size=14),
        legend=dict(x=0.8, y=1.1, orientation='h')
    )
    st.plotly_chart(fig_bar)

    st.subheader('Medal Distribution')
    medal_dist = filtered_data[['Gold', 'Silver', 'Bronze']].sum().reset_index()
    medal_dist.columns = ['Medal', 'Count']

    fig_pie = px.pie(medal_dist, values='Count', names='Medal',
                     title=f'Medal Distribution for {selected_noc}',
                     labels={'Count': 'Medal Count'},
                     color_discrete_map={'Gold': 'gold', 'Silver': 'silver', 'Bronze': '#cd7f32'})
    fig_pie.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        title_font=dict(size=14)
    )
    st.plotly_chart(fig_pie)

else:
    st.write("No data available for the selected filters.")

# Footer
st.markdown("Data source: [Olympics Dataset on Kaggle](https://www.kaggle.com/code/youssefismail20/olympics-1994-2024)")

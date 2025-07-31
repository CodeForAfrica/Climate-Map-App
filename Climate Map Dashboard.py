import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

st.set_page_config(layout="wide", page_title="Climate Map Africa", page_icon="🌍")

# Enhanced CSS styling with SDG colors and climate imagery

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    html, body, [class*="st"] {
        font-family: 'Poppins', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    .stApp {
        background-image: url("https://climatemapped-africa.dev.codeforafrica.org/_next/static/media/bg-map-white.f3fbc71d.jpg");
        background-attachment: fixed;
        background-size: cover;
    }
        #.custom-container {
        #    background-image: 
        #    background-size: cover;  
        #    background-position: center; 
        #    background-repeat: no-repeat; 
        #    #background-color: #ffeaa7;
        #    padding: 20px;
        #    border-radius: 10px;
        #    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        .main-title {
            background-image: url("https://climatemapped-africa.dev.codeforafrica.org/media/sat-mtKenya-1_alt@2400x.jpg");
            background-size: cover;
            background-position: center;
            #background: linear-gradient(135deg, #0000FF 0%, #0000FF 100%);
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            color: white;
            font-size: 42px;
            font-weight: bold;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            #border: 2px solid #FFD700;
        }

        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .sdg-header {
            background: linear-gradient(90deg, #FF0000, #007aff, #45B7D1, #0000FF, #0000FF);
            background-size: 300% 300%;
            animation: gradientShift 3s ease infinite;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            color: white;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .climate-warning {
            background: linear-gradient(135deg, #FF4444 0%, #CC0000 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
            font-weight: bold;
            text-align: center;
            margin: 20px 0;
            box-shadow: 0 4px 15px rgba(255,68,68,0.3);
            border-left: 5px solid #FFD700;
        }
        
        .climate-info {
            #background: linear-gradient(135deg, #007aff 0%, #007aff 100%);
            #background: linear-gradient(135deg, rgba(0,0,255,0.6) 0%, rgba(0,0,255,0.6) 100%);
            background: transparent;
            padding: 15px;
            border-radius: 8px;
            color: white;
            margin: 15px 0;
            box-shadow: 0 4px 15px rgba(78,205,196,0.3);
        }
        .climate-info h4 {
        color: black; 
        }
        .climate-info p {
        color: black;
        }
        
    
        .climate-good {
            #background: transparent;
            background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
            padding: 15px;
            border-radius: 8px;
            color: white;
            margin: 15px 0;
            box-shadow: 0 4px 15px rgba(86,171,47,0.3);
        }
        
        .subtitle {
            background-image: url("https://climatemapped-africa.dev.codeforafrica.org/media/sat-mtKenya-1_alt@2400x.jpg");
            background-size: cover;
            background-position: center;
            #background: linear-gradient(135deg, #0000FF 0%, #0000FF 100%);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            color: white;
            font-size: 22px;
            font-weight: bold;
            margin: 20px 0;
            #box-shadow: 0 4px 15px rgba(102,126,234,0.3);
            box-shadow: 0 4px 15px rgba(78,205,196,0.3);
        }
        
        .sdg-card {
            background: transparent;
            #background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 20px;
            border-radius: 12px;
            color: white;
            margin: 15px 0;
            #box-shadow: 0 6px 20px rgba(240,147,251,0.3);
            box-shadow: 0 4px 15px rgba(78,205,196,0.3);
        }

        }
        .sdg-card h4 {
        color: black; 
        }
        .sdg-card p {
        color: black;
        }
        
        .stats-card-1 {
            #background: linear-gradient(135deg, #4facfe 0%, #4facfe 100%);
            background: #0000CD; 
            padding: 20px;
            border-radius: 12px;
            color: white;
            text-align: center;
            margin: 10px 0;
            #box-shadow: 0 4px 15px rgba(79,172,254,0.3); 
            box-shadow: 0 4px 15px rgba(78,205,196,0.3);
            }
        .stats-card-1, 
        .stats-card-1 * {
            color: white ;
        }
            

        .stats-card-1:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 40px rgba(79, 172, 254, 0.5);
        }

        .stats-card-2 {
            #background: linear-gradient(135deg, #7B68EE 0%, #7B68EE 100%);
            background: #1E90FF;
            padding: 20px;
            border-radius: 12px;
            color: white;
            text-align: center;
            margin: 10px 0;
            #box-shadow: 0 4px 15px rgba(67,233,123,0.3);
            box-shadow: 0 4px 15px rgba(78,205,196,0.3);
        }

        .stats-card-2, 
        .stats-card-2 * {
            color: white ;
        }

        .stats-card-2:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 40px rgba(79, 172, 254, 0.5);
        }
        
        .stats-card-3 {
            #background: linear-gradient(135deg, #1E90FF 0%, #1E90FF 100%);
            background:#0000FF; 
            padding: 20px;
            border-radius: 12px;
            color: white;
            text-align: center;
            margin: 10px 0;
            #box-shadow: 0 4px 15px rgba(240,147,251,0.3);
            box-shadow: 0 4px 15px rgba(78,205,196,0.3);
        }

        .stats-card-3, 
        .stats-card-3 * {
            color: white ;
        }
        
        .stats-card-3:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 40px rgba(79, 172, 254, 0.5);
        }
        
        .stats-card-4 {
            #background: linear-gradient(135deg, #00BFFF 0%, #00BFFF 100%);
            background: #00BFFF;
            padding: 20px;
            border-radius: 12px;
            color: white;
            text-align: center;
            margin: 10px 0;
            #box-shadow: 0 4px 15px rgba(255,154,158,0.3);
            box-shadow: 0 4px 15px rgba(78,205,196,0.3);
        }

        .stats-card-4, 
        .stats-card-4 * {
            color: white ;
        }
        .stats-card-4:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 40px rgba(79, 172, 254, 0.5);
        }

        
        .footer {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-top: 30px;
        }
        
        .click-instruction {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 15px;
            border-radius: 8px;
            color: white;
            text-align: center;
            margin: 15px 0;
            box-shadow: 0 4px 15px rgba(102,126,234,0.3);
            font-size: 18px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Country code to country name mapping for African countries
country_mapping = {
    'DZ': 'Algeria', 'AO': 'Angola', 'BJ': 'Benin', 'BW': 'Botswana',
    'BF': 'Burkina Faso', 'BI': 'Burundi', 'CM': 'Cameroon', 'CV': 'Cape Verde',
    'CF': 'Central African Republic', 'TD': 'Chad', 'KM': 'Comoros', 'CG': 'Congo',
    'CD': 'Democratic Republic of Congo', 'CI': 'Côte d\'Ivoire', 'DJ': 'Djibouti',
    'EG': 'Egypt', 'EH': 'Western Sahara', 'GQ': 'Equatorial Guinea', 'ER': 'Eritrea', 'ET': 'Ethiopia', 
    'GA': 'Gabon', 'GM': 'Gambia', 'GH': 'Ghana', 'GN': 'Guinea', 'GW': 'Guinea-Bissau',
    'KE': 'Kenya', 'LS': 'Lesotho', 'LR': 'Liberia', 'LY': 'Libya', 'MG': 'Madagascar',
    'MW': 'Malawi', 'ML': 'Mali', 'MR': 'Mauritania', 'MU': 'Mauritius',
    'MA': 'Morocco', 'MZ': 'Mozambique', 'NA': 'Namibia', 'NE': 'Niger',
    'NG': 'Nigeria', 'RW': 'Rwanda', 'ST': 'São Tomé and Príncipe', 'SN': 'Senegal',
    'SC': 'Seychelles', 'SL': 'Sierra Leone', 'SO': 'Somalia', 'ZA': 'South Africa',
    'SS': 'South Sudan', 'SD': 'Sudan', 'SZ': 'Eswatini', 'TZ': 'Tanzania',
    'TG': 'Togo', 'TN': 'Tunisia', 'UG': 'Uganda', 'ZM': 'Zambia', 'ZW': 'Zimbabwe'
}

# Load and prepare the dataset
@st.cache_data
def load_data():
    # Load historical data
    df1 = pd.read_csv("sample_temp_1950-2025_1.csv")
    df2 = pd.read_csv("sample_temp_1950-2025_2.csv")
    df = pd.concat([df1, df2], axis=0).reset_index(drop=True)
    df.fillna("NA", inplace=True)
    df.columns = df.columns.str.lower()

    if 'latitude' not in df.columns:
        df['latitude'] = df['lat']
    if 'lng' not in df.columns and 'longitude' in df.columns:
        df['lng'] = df['longitude']

    df['country_name'] = df['country'].map(country_mapping)
    
    # Load prediction data
    df_pred = pd.read_csv("monthly_pred_temp_2025-2029.csv")
    df_pred.fillna("NA", inplace=True)
    df_pred.columns = df_pred.columns.str.lower()

    if 'latitude' not in df_pred.columns:
        df_pred['latitude'] = df_pred['lat']
    if 'lng' not in df_pred.columns and 'longitude' in df_pred.columns:
        df_pred['lng'] = df_pred['longitude']

    df_pred['country_name'] = df_pred['country'].map(country_mapping)
    
    return df, df_pred

def calculate_temperature_anomaly(df, baseline_start=1961, baseline_end=1990):
    """Calculate temperature anomaly based on baseline period (1961-1990)"""
    anomaly_df = df.copy()
    
    # Calculate baseline temperature for each city
    baseline_data = df[(df['year'] >= baseline_start) & (df['year'] <= baseline_end)]
    baseline_temps = baseline_data.groupby('city')['temperature'].mean().reset_index()
    baseline_temps.columns = ['city', 'baseline_temp']
    
    # Merge with main dataframe
    anomaly_df = anomaly_df.merge(baseline_temps, on='city', how='left')
    
    # Calculate anomaly
    anomaly_df['temperature_anomaly'] = anomaly_df['temperature'] - anomaly_df['baseline_temp']
    
    return anomaly_df

def calculate_prediction_anomaly(df_pred, baseline_temps):
    """Calculate temperature anomaly for prediction data using historical baseline"""
    anomaly_df = df_pred.copy()
    
    # Merge with baseline temperatures
    anomaly_df = anomaly_df.merge(baseline_temps, on='city', how='left')
    
    # Calculate anomaly
    anomaly_df['temperature_anomaly'] = anomaly_df['temperature'] - anomaly_df['baseline_temp']
    
    return anomaly_df

def generate_climate_narrative(city_data, city_name, country_name):
    """Generate dynamic climate narrative based on data"""
    if city_data.empty:
        return ""
    
    # Calculate trends and anomalies
    recent_years = city_data[city_data['year'] >= 2015]
    early_years = city_data[city_data['year'] <= 1980]
    
    if not recent_years.empty and not early_years.empty:
        recent_avg = recent_years['temperature'].mean()
        early_avg = early_years['temperature'].mean()
        temp_change = recent_avg - early_avg
        
        # Get latest anomaly
        latest_anomaly = city_data[city_data['year'] == city_data['year'].max()]['temperature_anomaly'].iloc[0]
        
        # Generate narrative based on temperature trends
        if temp_change > 2.0:
            narrative_class = "climate-warning"
            emoji = "🔥"
            title = "CRITICAL TEMPERATURE RISE DETECTED"
            message = f"""
            <div class="{narrative_class}">
                <h3>{emoji} {title} {emoji}</h3>
                <p><strong>{city_name}, {country_name}</strong> has experienced a significant temperature increase of 
                <strong>{temp_change:.1f}°C</strong> since the 1980s!</p>
                <p>Current anomaly: <strong>{latest_anomaly:+.1f}°C</strong> above the 1961-1990 baseline</p>
                <p>This aligns with <strong>SDG 13: Climate Action</strong> - urgent action needed to combat climate change!</p>
                <p> <strong>Take Action:</strong> Act now. First and foremost, by urging all levels of government to give climate action top priority and allocate resources accordingly. Furthermore, mitigation should be a local issue that 
                is addressed in households, communities, schools, and places of worship rather than just being a national one.</p>
            </div>
            """
        elif temp_change > 1.0:
            narrative_class = "climate-info"
            emoji = "⚠️"
            title = "MODERATE WARMING TREND"
            message = f"""
            <div class="{narrative_class}">
                <h3 style="color: black;">{emoji} {title} {emoji}</h3>
                <p><strong>{city_name}, {country_name}</strong> shows a moderate warming trend of 
                <strong>{temp_change:.1f}°C</strong> since the 1980s.</p>
                <p>Current anomaly: <strong>{latest_anomaly:+.1f}°C</strong> above the 1961-1990 baseline</p>
                <p> This relates to <strong>SDG 13: Climate Action</strong> and <strong>SDG 11: Sustainable Cities</strong></p>
                <p> Monitor trends closely and implement adaptation strategies.</p>
            </div>
            """
        else:
            narrative_class = "climate-good"
            emoji = "✅"
            title = "STABLE TEMPERATURE PATTERN"
            message = f"""
            <div class="{narrative_class}">
                <h3>{emoji} {title} {emoji}</h3>
                <p><strong>{city_name}, {country_name}</strong> shows relatively stable temperatures with a change of 
                <strong>{temp_change:.1f}°C</strong> since the 1980s.</p>
                <p>Current anomaly: <strong>{latest_anomaly:+.1f}°C</strong> compared to the 1961-1990 baseline</p>
                <p>🌱 Continue supporting <strong>SDG 13: Climate Action</strong> to maintain stability!</p>
            </div>
            """
        
        return message
    
    return ""

def create_climate_heatmap(df, selected_city):
    """Create an enhanced climate stripes style heatmap with anomaly data for a single city"""
    if not selected_city:
        return None
    
    # Filter data for selected city
    city_data = df[df['city'] == selected_city]
    
    if city_data.empty:
        return None
    
    # Sort by year
    city_data = city_data.sort_values('year')
    
    # Create heatmap with anomaly scale (single row for the city)
    fig = go.Figure(data=go.Heatmap(
        z=[city_data['temperature_anomaly'].values],
        x=city_data['year'].values,
        y=[selected_city],
        zmin=-3,
        zmax=3,
        colorscale='RdBu_r',
        showscale=False,
        hovertemplate='<b>%{y}</b><br>' +
                      'Year: %{x}<br>' +
                      'Anomaly: %{z:.2f}°C<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"Historical Temperature Anomalies for {selected_city}",
        paper_bgcolor='rgba(255,255,255,0.95)',
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis_title="Year",
        yaxis=dict(showticklabels=False, gridcolor='rgba(0,0,0,0.1)'),
        height=350,
        font=dict(size=12),
        title_font=dict(size=16, color='#2c3e50'),
        xaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
        autosize=True
    )
    
    return fig

def create_prediction_heatmap(df_pred, selected_city):
    """Create a climate stripes style heatmap for prediction data"""
    if not selected_city:
        return None
    
    # Filter data for selected city
    city_data = df_pred[df_pred['city'] == selected_city]
    
    if city_data.empty:
        return None
    
    # Sort by date and extract year for x-axis
    city_data = city_data.sort_values('date')
    
    # Convert date to datetime if it's not already and extract year
    if not pd.api.types.is_datetime64_any_dtype(city_data['date']):
        city_data['date'] = pd.to_datetime(city_data['date'])
    
    # Create year column for heatmap x-axis
    city_data['year'] = city_data['date'].dt.year
    
    # Create heatmap with anomaly scale (single row for the city)
    fig = go.Figure(data=go.Heatmap(
        z=[city_data['temperature_anomaly'].values],
        x=city_data['date'].values,
        y=[selected_city],
        zmin=-3,
        zmax=3,
        colorscale='RdBu_r',
        showscale=False,
        hovertemplate='<b>%{y}</b><br>' +
                      'Date: %{x}<br>' +
                      'Predicted Anomaly: %{z:.2f}°C<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"Predicted Temperature Anomalies for {selected_city} (2025-2029)",
        paper_bgcolor='rgba(255,255,255,0.95)',
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis_title="Date",
        yaxis=dict(showticklabels=False, gridcolor='rgba(0,0,0,0.1)'),
        height=350,
        font=dict(size=12),
        title_font=dict(size=16, color='#2c3e50'),
        xaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
        autosize=True
    )
    
    return fig

def create_temperature_trend_chart(df, selected_city):
    """Create a line chart showing temperature trends for the selected city"""
    if not selected_city:
        return None
    
    city_data = df[df['city'] == selected_city].sort_values('year')
    
    if city_data.empty:
        return None
    
    fig = go.Figure()
    
    # Add temperature line
    fig.add_trace(go.Scatter(
        x=city_data['year'],
        y=city_data['temperature'],
        mode='lines+markers',
        name='Historical Temperature',
        line=dict(color='#4B9CD3', width=3),
        marker=dict(size=6, color='#4B9CD3'),
        hovertemplate='Year: %{x}<br>Temperature: %{y:.1f}°C<extra></extra>'
    ))
    
    # Add trend line
    z = np.polyfit(city_data['year'], city_data['temperature'], 1)
    p = np.poly1d(z)
    fig.add_trace(go.Scatter(
        x=city_data['year'],
        y=p(city_data['year']),
        mode='lines',
        name='Historical Trend',
        line=dict(color='#FF0000', width=4, dash='dash'),
        hovertemplate='Year: %{x}<br>Trend: %{y:.1f}°C<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"Historical Temperature Trend for {selected_city}",
        plot_bgcolor='rgba(255,255,255,0.9)',
        paper_bgcolor='rgba(255,255,255,0.95)',
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis_title="Year",
        yaxis_title="Temperature (°C)",
        height=350,
        font=dict(size=12),
        title_font=dict(size=16, color='#2c3e50'),
        xaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
        legend=dict(
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='rgba(0,0,0,0.2)',
            borderwidth=1
        ),
        autosize=True
    )
    
    return fig

def create_prediction_trend_chart(df_pred, selected_city):
    """Create a line chart showing predicted temperature trends for the selected city"""
    if not selected_city:
        return None
    
    city_data = df_pred[df_pred['city'] == selected_city].sort_values('year')
    
    if city_data.empty:
        return None
    
    fig = go.Figure()
    
    # Add predicted temperature line
    fig.add_trace(go.Scatter(
        x=city_data['year'],
        y=city_data['temperature'],
        mode='lines+markers',
        name='Predicted Temperature',
        line=dict(color='#FF8C00', width=3),
        marker=dict(size=6, color='#FF8C00'),
        hovertemplate='Year: %{x}<br>Predicted Temperature: %{y:.1f}°C<extra></extra>'
    ))
    
    # Add prediction trend line
    z = np.polyfit(city_data['year'], city_data['temperature'], 1)
    p = np.poly1d(z)
    fig.add_trace(go.Scatter(
        x=city_data['year'],
        y=p(city_data['year']),
        mode='lines',
        name='Prediction Trend',
        line=dict(color='#DC143C', width=4, dash='dash'),
        hovertemplate='Year: %{x}<br>Trend: %{y:.1f}°C<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"Predicted Temperature Trend for {selected_city} (2025-2029)",
        plot_bgcolor='rgba(255,255,255,0.9)',
        paper_bgcolor='rgba(255,255,255,0.95)',
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis_title="Year",
        yaxis_title="Temperature (°C)",
        height=350,
        font=dict(size=12),
        title_font=dict(size=16, color='#2c3e50'),
        xaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
        legend=dict(
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='rgba(0,0,0,0.2)',
            borderwidth=1
        ),
        autosize=True
    )
    
    return fig

def create_combined_trend_chart(df, df_pred, selected_city):
    """Create a combined chart showing both historical and predicted temperature trends"""
    if not selected_city:
        return None
    
    historical_data = df[df['city'] == selected_city].sort_values('year')
    prediction_data = df_pred[df_pred['city'] == selected_city].sort_values('year')
    
    if historical_data.empty and prediction_data.empty:
        return None
    
    fig = go.Figure()
    
    # Add historical temperature line
    if not historical_data.empty:
        fig.add_trace(go.Scatter(
            x=historical_data['year'],
            y=historical_data['temperature'],
            mode='lines+markers',
            name='Historical Temperature',
            line=dict(color='#4B9CD3', width=3),
            marker=dict(size=4, color='#4B9CD3'),
            hovertemplate='Year: %{x}<br>Temperature: %{y:.1f}°C<extra></extra>'
        ))
        
        # Add historical trend line
        z_hist = np.polyfit(historical_data['year'], historical_data['temperature'], 1)
        p_hist = np.poly1d(z_hist)
        fig.add_trace(go.Scatter(
            x=historical_data['year'],
            y=p_hist(historical_data['year']),
            mode='lines',
            name='Historical Trend',
            line=dict(color='#FF0000', width=3, dash='dash'),
            hovertemplate='Year: %{x}<br>Historical Trend: %{y:.1f}°C<extra></extra>'
        ))
    
    # Add predicted temperature line
    if not prediction_data.empty:
        fig.add_trace(go.Scatter(
            x=prediction_data['year'],
            y=prediction_data['temperature'],
            mode='lines+markers',
            name='Predicted Temperature',
            line=dict(color='#FF8C00', width=3),
            marker=dict(size=4, color='#FF8C00'),
            hovertemplate='Year: %{x}<br>Predicted Temperature: %{y:.1f}°C<extra></extra>'
        ))
        
        # Add prediction trend line
        z_pred = np.polyfit(prediction_data['year'], prediction_data['temperature'], 1)
        p_pred = np.poly1d(z_pred)
        fig.add_trace(go.Scatter(
            x=prediction_data['year'],
            y=p_pred(prediction_data['year']),
            mode='lines',
            name='Prediction Trend',
            line=dict(color='#DC143C', width=3, dash='dot'),
            hovertemplate='Year: %{x}<br>Prediction Trend: %{y:.1f}°C<extra></extra>'
        ))
    
    fig.update_layout(
        title=f"Historical & Predicted Temperature Trends for {selected_city}",
        plot_bgcolor='rgba(255,255,255,0.9)',
        paper_bgcolor='rgba(255,255,255,0.95)',
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis_title="Year",
        yaxis_title="Temperature (°C)",
        height=400,
        font=dict(size=12),
        title_font=dict(size=16, color='#2c3e50'),
        xaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
        legend=dict(
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='rgba(0,0,0,0.2)',
            borderwidth=1
        ),
        autosize=True
    )
    
    return fig

# Initialize session state for selected city
if 'selected_city' not in st.session_state:
    st.session_state.selected_city = None

# Main App
st.markdown("""
    <div class="main-title">
        Climate Map Africa
    </div>
""", unsafe_allow_html=True)

# Load data and calculate anomalies
data_result = load_data()

# Check if data loading was successful
if data_result[0] is None:
    st.error("❌ Failed to load data. Please check your CSV files.")
    st.stop()

df, df_pred = data_result

# Only proceed if we have historical data
if df is not None:
    df = calculate_temperature_anomaly(df)
    
    # Calculate baseline temperatures for predictions (only if we have prediction data)
    if df_pred is not None:
        baseline_data = df[(df['year'] >= 1961) & (df['year'] <= 1990)]
        baseline_temps = baseline_data.groupby('city')['temperature'].mean().reset_index()
        baseline_temps.columns = ['city', 'baseline_temp']
        
        # Calculate anomalies for prediction data
        df_pred = calculate_prediction_anomaly(df_pred, baseline_temps)
        st.success("✅ Both historical and prediction data loaded successfully!")
    else:
        st.warning("⚠️ Only historical data available. Prediction features will be disabled.")
else:
    st.error("❌ No data available. Please check your files.")
    st.stop()

# Display key statistics
latest_year = df['year'].max()
latest_data = df[df['year'] == latest_year]

with st.container():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class="stats-card-1">
                <h5>Cities and Towns Monitored</h5>
                <h2>{len(df['city'].unique())}</h2>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="stats-card-2">
                <h5>Countries Covered</h5>
                <h2>{len(df['country_name'].unique())}</h2>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        avg_temp = latest_data['temperature'].mean()
        st.markdown(f"""
            <div class="stats-card-3">
                <h5>Average Temperature {latest_year}</h5>
                <h2>{avg_temp:.1f}°C</h2>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        avg_anomaly = latest_data['temperature_anomaly'].mean()
        st.markdown(f"""
            <div class="stats-card-4">
                <h5>Average Anomaly {latest_year}</h5>
                <h2>{avg_anomaly:+.1f}°C</h2>
            </div>
        """, unsafe_allow_html=True)

st.markdown("""
        <div class="climate-info">
            <h4>🎯 Get Started:</h4>
            <p>Use the country and city selection boxes below to choose specific locations for analysis.</p>
            <p>Or click on any city point on the map above to begin your climate analysis journey!</p>
            <p>Explore how temperatures have changed over time and discover the impacts of climate change in Africa.</p>
        </div>
    """, unsafe_allow_html=True)

# Country and city selection (appears first for better UX)
countries = sorted(df['country_name'].dropna().unique())

# Create two columns for aligned filters
col1, col2 = st.columns(2)

with col1:
    selected_countries = st.multiselect(
        "Select countries to analyze:", 
        countries, 
        default=[],
        help="Choose one or more African countries to examine their climate data"
    )

# Filter cities based on selected countries
available_cities = df[df['country_name'].isin(selected_countries)]['city'].sort_values().unique() if selected_countries else []

with col2:
    selected_cities = st.multiselect(
        "Select cities for detailed analysis:", 
        available_cities, 
        default=[],
        help="Choose specific cities to analyze temperature trends and anomalies"
    )

# Default center and zoom
map_center = {"lat": 0, "lon": 20}
map_zoom = 2

# If only one city is selected, zoom into it
if len(selected_cities) == 1:
    city_info = df[df['city'] == selected_cities[0]].iloc[0]
    map_center = {"lat": city_info["latitude"], "lon": city_info["lng"]}
    map_zoom = 12

fig_map = px.scatter_mapbox(
    latest_data,
    lat="latitude",
    lon="lng",
    color="temperature",
    hover_name="city",
    hover_data={"temperature": ":.1f", "country_name": True},
    center=map_center,
    zoom=map_zoom,
    mapbox_style="open-street-map",
    color_continuous_scale="RdBu_r",
)

# Set marker size after creation
fig_map.update_traces(marker=dict(size=13))
fig_map.update_layout(height=700, width=1500, margin=dict(l=0, r=0, t=30, b=0))
fig_map.update_layout(
    coloraxis_colorbar=dict(
        title="Average Temperature(°C) 2025",
        title_side='top',
        title_font=dict(
            color='black',        
            size=14              
        ),
        tickfont=dict(
            color='black',     
            size=12            
        ),
        x=0.70,                 
        y=0.05,                 
        xanchor='left',
        yanchor='bottom',
        orientation='h',        
        len=0.3,                
        thickness=15            
    )
)
fig_map.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
)

# Display the map and capture click events
map_click = st.plotly_chart(fig_map, use_container_width=True, on_select="rerun")

# Handle map click events
if map_click and map_click.selection and map_click.selection.points:
    # Get the clicked point
    clicked_point = map_click.selection.points[0]
    
    # Find the city based on the clicked point's hover_name
    if 'hovertext' in clicked_point:
        clicked_city = clicked_point['hovertext']
        st.session_state.selected_city = clicked_city
    elif 'customdata' in clicked_point:
        # Alternative method to get city name
        point_index = clicked_point['point_index']
        if point_index < len(latest_data):
            clicked_city = latest_data.iloc[point_index]['city']
            st.session_state.selected_city = clicked_city

# Display analysis for selected city from map click (only if actually clicked)
if st.session_state.selected_city is not None:
    selected_city = st.session_state.selected_city

    # Get city data
    city_data = df[df['city'] == selected_city]
    city_pred_data = df_pred[df_pred['city'] == selected_city] if df_pred is not None else pd.DataFrame()

    if not city_data.empty:
        country_name = city_data['country_name'].iloc[0]

        st.markdown(f"""
            <div class="subtitle">
                Detailed Climate Analysis for {selected_city}, {country_name}
            </div>
        """, unsafe_allow_html=True)

        # Historical Analysis Section
        st.markdown("### Historical Analysis")
        col1, col2 = st.columns(2)

        with col1:
            trend_chart = create_temperature_trend_chart(df, selected_city)
            st.plotly_chart(trend_chart, use_container_width=True)

        with col2:
            heatmap = create_climate_heatmap(df, selected_city)
            st.plotly_chart(heatmap, use_container_width=True)

        narrative = generate_climate_narrative(city_data, selected_city, country_name)
        st.markdown(narrative, unsafe_allow_html=True)
        
        # ================= Prediction Analysis Section =================
if df_pred is not None:
    # Prepare prediction data only once
    df_pred_processed = df_pred.copy()
    
    # Parse date if present (e.g., "Jul-2025")
    if 'date' in df_pred.columns:
        df_pred_processed['date_parsed'] = pd.to_datetime(
            df_pred_processed['date'], format='%b-%Y'
        )
        df_pred_processed['year'] = df_pred_processed['date_parsed'].dt.year
        df_pred_processed['month'] = df_pred_processed['date_parsed'].dt.month

# Display analysis for selected cities
if selected_cities:
    for city in selected_cities:
        city_data = df[df['city'] == city].copy()
        if city_data.empty:
            continue

        country_name = city_data['country_name'].iloc[0]
        st.markdown(f"""
            <div class="subtitle">
                Detailed Climate Analysis for {city}, {country_name}
            </div>
        """, unsafe_allow_html=True)

        # ---------------- Historical Analysis ----------------
        st.markdown("### Historical Analysis")
        col1, col2 = st.columns(2)

        with col1:
            trend_chart = create_temperature_trend_chart(df, city)
            st.plotly_chart(trend_chart, use_container_width=True)

        with col2:
            heatmap = create_climate_heatmap(df, city)
            st.plotly_chart(heatmap, use_container_width=True)

        # Optional narrative
        narrative = generate_climate_narrative(city_data, city, country_name)
        if narrative:
            st.markdown(narrative, unsafe_allow_html=True)

        # ================= Prediction Analysis Section =================
if df_pred is not None:
    # Prepare prediction data only once
    df_pred_processed = df_pred.copy()

    # Parse date if present (e.g., "Jul-2025")
    if 'date' in df_pred.columns:
        df_pred_processed['date_parsed'] = pd.to_datetime(
            df_pred_processed['date'], format='%b-%Y'
        )
        df_pred_processed['year'] = df_pred_processed['date_parsed'].dt.year
        df_pred_processed['month'] = df_pred_processed['date_parsed'].dt.month

# Display analysis for selected cities
if selected_cities:
    for city in selected_cities:
        city_data = df[df['city'] == city].copy()
        if city_data.empty:
            continue

        country_name = city_data['country_name'].iloc[0]
        st.markdown(f"""
            <div class="subtitle">
                Detailed Climate Analysis for {city}, {country_name}
            </div>
        """, unsafe_allow_html=True)

        # ---------------- Historical Analysis ----------------
        st.markdown("### Historical Analysis")
        col1, col2 = st.columns(2)

        # Aggregate historical data by year for trend plot
        hist_yearly = city_data.groupby('year', as_index=False).agg({'temperature':'mean'})
        
        with col1:
            trend_chart = px.line(
                hist_yearly,
                x='year', y='temperature',
                title=f"Historical Temperature Trend - {city}",
                markers=True
            )
            st.plotly_chart(trend_chart, use_container_width=True)

        with col2:
            heatmap = create_climate_heatmap(df, city)  # Already has month x year format
            st.plotly_chart(heatmap, use_container_width=True)

        # Optional narrative
        narrative = generate_climate_narrative(city_data, city, country_name)
        if narrative:
            st.markdown(narrative, unsafe_allow_html=True)

        # ---------------- Prediction Analysis ----------------
        city_pred_data = pd.DataFrame()
        if df_pred is not None:
            city_pred_data = df_pred_processed[df_pred_processed['city'] == city]

        if not city_pred_data.empty:
            st.markdown("### Future Predictions (2025-2029)")

            # 1️⃣ Aggregate predicted temperatures annually
            pred_yearly = city_pred_data.groupby('year', as_index=False).agg({'temperature':'mean'})

            # 2️⃣ Combined Historical + Predicted Trend
            combined_yearly = pd.concat([
                hist_yearly.assign(type='Historical'),
                pred_yearly.assign(type='Predicted')
            ])
            combined_chart = px.line(
                combined_yearly,
                x='year', y='temperature',
                color='type',
                title=f"Historical vs Predicted Temperature Trend - {city}",
                markers=True
            )
            st.plotly_chart(combined_chart, use_container_width=True)

            col3, col4 = st.columns(2)

            # 3️⃣ Annual Predicted Temperature Trend
            with col3:
                pred_trend_chart = px.bar(
                    pred_yearly,
                    x='year', y='temperature',
                    title=f"Predicted Annual Temperature - {city}",
                    text_auto='.1f'
                )
                st.plotly_chart(pred_trend_chart, use_container_width=True)

            # 4️⃣ Predicted Anomaly Heatmap (Month vs Year)
            with col4:
                heatmap_data = city_pred_data.pivot_table(
                    index='month', columns='year', values='temperature_anomaly', aggfunc='mean'
                )
                # Convert month numbers to labels
                heatmap_data.index = heatmap_data.index.map(lambda x: calendar.month_abbr[x])

                pred_heatmap = px.imshow(
                    heatmap_data,
                    aspect='auto',
                    color_continuous_scale='RdBu_r',
                    title=f"Predicted Temperature Anomalies (Month-Year) - {city}"
                )
                st.plotly_chart(pred_heatmap, use_container_width=True)

            # Prediction Summary
            avg_pred_temp = city_pred_data['temperature'].mean()
            avg_pred_anomaly = city_pred_data['temperature_anomaly'].mean()
            
            if 'date_parsed' in city_pred_data.columns:
                min_date = city_pred_data['date_parsed'].min()
                max_date = city_pred_data['date_parsed'].max()
                date_range = f"({min_date.strftime('%b/%Y')} - {max_date.strftime('%b/%Y')})"
            else:
                date_range = "(2025-2029)"
            
            st.markdown(f"""
                <div class="climate-info">
                    <h4>Prediction Summary for {city}</h4>
                    <p><strong>Average Predicted Temperature {date_range}:</strong> {avg_pred_temp:.1f}°C</p>
                    <p><strong>Average Predicted Anomaly:</strong> {avg_pred_anomaly:+.1f}°C above 1961-1990 baseline</p>
                    <p>These predictions help inform climate adaptation and mitigation strategies.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info(f"ℹ️ No prediction data available for {city}.")

# Clear selection button
if st.button("Clear Selection", key="clear_selection"):
    st.session_state.selected_city = None
    st.rerun()

            
## Show help message when no selections are made
#if st.session_state.selected_city is None and not selected_cities:
#    st.markdown("""
#        <div class="climate-info">
#            <h4>🎯 Get Started:</h4>
#            <p>Use the country and city selection boxes above to choose specific locations for analysis.</p>
#            <p>Or click on any city point on the map above to begin your climate analysis journey!</p>
#            <p>Explore how temperatures have changed over time and discover the impacts of climate change in Africa.</p>
#        </div>
#    """, unsafe_allow_html=True)

    
#st.markdown("---")
    
# Additional insights
#st.markdown("""
#            <div class="climate-info">
#                <h4>📖 Understanding Temperature Anomalies:</h4>
#                <p>• <strong>Positive anomalies (red)</strong>: Temperatures above the 1961-1990 average</p>
#                <p>• <strong>Negative anomalies (blue)</strong>: Temperatures below the 1961-1990 average</p>
#                <p>• <strong>Baseline period</strong>: 1961-1990 is used as the reference period following WMO standards</p>
#                <p>• <strong>Climate stripes</strong>: Each column represents one year, showing long-term trends</p>
#            </div>
#""", unsafe_allow_html=True)


# SDG Information Section

with st.container():
    st.markdown("""
    <div class="sdg-header" style="text-align:center;">
        🎯 Supporting UN Sustainable Development Goals 🎯 
    </div>
""", unsafe_allow_html=True)


    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="sdg-card">
                <h4>🌍 SDG 13: Climate Action</h4>
                <p>Take urgent action to combat climate change and its impacts through monitoring trends and promoting awareness.</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="sdg-card">
                <h4>🏙️ SDG 11: Sustainable Cities</h4>
                <p>Make cities and human settlements inclusive, safe, resilient and sustainable by understanding urban climate patterns.</p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="sdg-card">
                <h4>🤝 SDG 17: Partnerships</h4>
                <p>Strengthen global partnerships for sustainable development through open climate data and knowledge sharing.</p>
            </div>
        """, unsafe_allow_html=True)
        

# Call to Action
st.markdown("""
    <div class="sdg-card">
        <h3 style="color: black;">🌱 Take Climate Action Today!</h3>
        <p>Support renewable energy, reduce carbon footprint, and advocate for climate policies. Small and smart choices to mitigate increasing temperatures:</p>
        <ul style="color: black;">
          <li>Create green spaces like parks, urban forests, rooftop gardens, community gardens, and green roofs or walls.</li>
          <li>Plant native species to promote biodiversity.</li>
          <li>Use renewable energy sources and improve energy efficiency.</li>
          <li>Walk, bike, or take public transport to reduce greenhouse gas emissions.</li>
          <li>Reduce, reuse, repair, and recycle to lower your carbon footprint.</li>
          <li>Advocate for change: speak up and encourage others to take action.</li>
        </ul>

    </div>

""", unsafe_allow_html=True)

st.markdown("---")

# Footer
st.markdown("""
    <div class="footer">
        <h4 style="color: white;" >🌍 Climate Map Africa Dashboard</h4>
        <p>Data source: <a href="https://cds.climate.copernicus.eu/" target="_blank" style="color: #4ECDC4;">Copernicus Climate Data Store</a></p>
        <p>Supporting UN SDGs: Climate Action (13) • Sustainable Cities (11) • Partnerships (17)</p>
        <p>🤝 Together, we can build a sustainable future for Africa and the world!</p>
    </div>
""", unsafe_allow_html=True)

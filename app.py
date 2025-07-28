from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.utils
import numpy as np
import json
from datetime import datetime

app = Flask(__name__)

# Google Sheets configuration
sheet_id = '1thMQ4ndtgzyEM6qfoA2tfrt3MEzZY2CtxhjpCTNcS0U'
content_sheet_name = 'Content'
follower_sheet = 'Sheet24'
location_sheet = 'Sheet25'
job_function_sheet = 'Sheet26'
industry_sheet = 'Sheet27'

# Construct the URLs for CSV export
content_csv_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={content_sheet_name}'
follower_csv_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={follower_sheet}'
location_sheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={location_sheet}'
job_function_sheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={job_function_sheet}'
industry_sheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={industry_sheet}'

def load_data():
    """Load all data from Google Sheets"""
    try:
        df = pd.read_csv(content_csv_url)
        follower_df = pd.read_csv(follower_csv_url)
        location_df = pd.read_csv(location_sheet_url)
        job_function_df = pd.read_csv(job_function_sheet_url)
        industry_df = pd.read_csv(industry_sheet_url)
        
        df['Created date'] = pd.to_datetime(df['Created date'])
        
        return df, follower_df, location_df, job_function_df, industry_df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None, None, None, None

def create_pie_chart(category, aggregate, dataframe, array):
    """Create pie chart data"""
    if not array:
        return None
    
    try:
        filtered_df = dataframe.groupby(category)[[aggregate]].sum()
        filtered_df = filtered_df.loc[array]
        data = {
            'Location': array,
            "Followers": filtered_df[aggregate].tolist()
        }
        convert_df = pd.DataFrame(data)
        fig = px.pie(convert_df, values='Followers', names='Location')
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    except Exception as e:
        print(f"Error creating pie chart: {e}")
        return None

def create_chart(category, aggregate, dataframe):
    """Create bar chart for filtered data"""
    try:
        group_keys = list(dataframe.groupby(category).groups.keys())
        filtered_df = dataframe.groupby(category)[[aggregate]].mean()
        post_count = list(dataframe.groupby(category)['Number of Post'].sum())
        filtered_df.insert(0, category, group_keys)
        filtered_df.insert(1, "Post Count", post_count)

        organize_time = []
        organize_number_posts = []
        organize_impressions = []

        if aggregate == 'Impressions' or aggregate == 'Clicks':
            for i in group_keys:
                organize_time.append(i)
                organize_number_posts.append(filtered_df.loc[filtered_df[category] == i]['Post Count'].values[0])
                organize_impressions.append(filtered_df.loc[filtered_df[category] == i][aggregate].values[0].round())

        elif aggregate == 'Engagement rate' or aggregate == 'Click through rate (CTR)':
            for i in group_keys:
                organize_time.append(i)
                organize_number_posts.append(filtered_df.loc[filtered_df[category] == i]['Post Count'].values[0])
                organize_impressions.append((filtered_df.loc[filtered_df[category] == i][aggregate].values[0]*100).round(2))

        data = {
            category: organize_time,
            "Number of Posts": organize_number_posts,
            aggregate: organize_impressions
        }

        fig = px.bar(data, x=category, y=aggregate, template='seaborn', color=category)
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder), data
    except Exception as e:
        print(f"Error creating chart: {e}")
        return None, None

@app.route('/')
def index():
    """Main page with default information"""
    df, follower_df, location_df, job_function_df, industry_df = load_data()
    
    if df is None:
        return render_template('error.html', message="Failed to load data from Google Sheets")
    
    # Create follower count chart
    try:
        data = {
            "Month/Yr": pd.to_datetime(follower_df['Date']).tolist(),
            "Follower": follower_df['Follower Count'].tolist()
        }
        follower_fig = go.Figure()
        follower_fig.add_trace(go.Scatter(x=data['Month/Yr'], y=data['Follower'], name='Follower Count'))
        follower_chart = json.dumps(follower_fig, cls=plotly.utils.PlotlyJSONEncoder)
    except Exception as e:
        print(f"Error creating follower chart: {e}")
        follower_chart = None
    
    # Create posting frequency chart
    try:
        post_count = df['Month & Year'].value_counts().sort_index()
        match_data = {month: post_count[month] for month in list(df['Month & Year'].unique())[::-1]}
        frequency_data = {
            "Month/Yr": list(match_data.keys()),
            "Number of Post": list(match_data.values())
        }
        frequency_fig = go.Figure()
        frequency_fig.add_trace(go.Scatter(x=frequency_data['Month/Yr'], y=frequency_data['Number of Post'], name='Post Frequency'))
        frequency_chart = json.dumps(frequency_fig, cls=plotly.utils.PlotlyJSONEncoder)
    except Exception as e:
        print(f"Error creating frequency chart: {e}")
        frequency_chart = None
        frequency_data = {}
    
    # Prepare data for demographics
    demographics_data = {
        'locations': location_df['Location'].tolist() if location_df is not None else [],
        'locations_view': location_df['Location View'].tolist() if location_df is not None else [],
        'job_functions': job_function_df['Job function'].tolist() if job_function_df is not None else [],
        'job_views': job_function_df['Job View'].tolist() if job_function_df is not None else [],
        'industries': industry_df['Industry'].tolist() if industry_df is not None else [],
        'industry_views': industry_df['Industry View'].tolist() if industry_df is not None else [],
    }
    
    return render_template('index.html', 
                           follower_chart=follower_chart,
                           frequency_chart=frequency_chart,
                           frequency_data=frequency_data,
                           demographics=demographics_data,
                           location_data=location_df.to_dict('records') if location_df is not None else [],
                           job_function_data=job_function_df.to_dict('records') if job_function_df is not None else [],
                           industry_data=industry_df.to_dict('records') if industry_df is not None else [])

@app.route('/filtered')
def filtered():
    """Filtered data page"""
    df, follower_df, location_df, job_function_df, industry_df = load_data()
    
    if df is None:
        return render_template('error.html', message="Failed to load data from Google Sheets")
    
    # Get date range
    startDate = pd.to_datetime(df["Created date"]).min()
    endDate = pd.to_datetime(df["Created date"]).max()
    
    # Get unique values for filters
    filter_options = {
        'years': df["Year"].unique().tolist(),
        'months': df["Month & Year"].unique().tolist(),
        'days': df["Day of the week"].unique().tolist(),
        'times': df["Interval Times"].unique().tolist(),
        'categories': df["Category"].unique().tolist(),
        'sub_categories': df["Sub-Category"].unique().tolist(),
        'emojis': df["Type Emoji"].unique().tolist(),
        'aggregates': ['Impressions', 'Clicks', 'Click through rate (CTR)', 'Engagement rate']
    }
    
    return render_template('filtered.html', 
                           filter_options=filter_options,
                           start_date=startDate.strftime('%Y-%m-%d'),
                           end_date=endDate.strftime('%Y-%m-%d'))

@app.route('/api/demographics/<chart_type>')
def api_demographics(chart_type):
    """API endpoint for demographics charts"""
    df, follower_df, location_df, job_function_df, industry_df = load_data()
    
    if df is None:
        return jsonify({'error': 'Failed to load data'})
    
    selected_items = request.args.getlist('items')
    
    chart_map = {
        'location_followers': ('Location', 'Total followers', location_df),
        'location_views': ('Location View', 'Total views', location_df),
        'job_followers': ('Job function', 'Total followers', job_function_df),
        'job_views': ('Job View', 'Total views', job_function_df),
        'industry_followers': ('Industry', 'Total followers', industry_df),
        'industry_views': ('Industry View', 'Total views', industry_df),
    }
    
    if chart_type not in chart_map:
        return jsonify({'error': 'Invalid chart type'})
    
    category, aggregate, dataframe = chart_map[chart_type]
    chart_json = create_pie_chart(category, aggregate, dataframe, selected_items)
    
    return jsonify({'chart': chart_json})

@app.route('/api/filtered_chart')
def api_filtered_chart():
    """API endpoint for filtered charts"""
    df, follower_df, location_df, job_function_df, industry_df = load_data()
    
    if df is None:
        return jsonify({'error': 'Failed to load data'})
    
    # Get filter parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    years = request.args.getlist('years')
    months = request.args.getlist('months')
    days = request.args.getlist('days')
    times = request.args.getlist('times')
    categories = request.args.getlist('categories')
    sub_categories = request.args.getlist('sub_categories')
    emojis = request.args.getlist('emojis')
    aggregates = request.args.getlist('aggregates')
    chart_category = request.args.get('chart_category')
    
    # Apply filters
    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        df = df[(df["Created date"] >= start_date) & (df["Created date"] <= end_date)].copy()
    
    if years:
        df = df[df["Year"].isin(years)]
    if months:
        df = df[df["Month & Year"].isin(months)]
    if days:
        df = df[df["Day of the week"].isin(days)]
    if times:
        df = df[df["Interval Times"].isin(times)]
    if categories:
        df = df[df["Category"].isin(categories)]
    if sub_categories:
        df = df[df["Sub-Category"].isin(sub_categories)]
    if emojis:
        df = df[df["Type Emoji"].isin(emojis)]
    
    # Create charts
    charts = {}
    tables = {}
    
    for aggregate in aggregates:
        if chart_category:
            chart_json, table_data = create_chart(chart_category, aggregate, df)
            charts[f"{chart_category}_{aggregate}"] = chart_json
            tables[f"{chart_category}_{aggregate}"] = table_data
    
    return jsonify({'charts': charts, 'tables': tables})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

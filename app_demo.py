from flask import Flask, render_template, request, jsonify
import plotly.express as px
import plotly.graph_objects as go
import plotly.utils
import numpy as np
import json
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# Demo data generators (replacing pandas functionality)
def generate_demo_data():
    """Generate demo data to simulate Google Sheets data"""
    
    # Generate dates for the last year
    dates = []
    start_date = datetime.now() - timedelta(days=365)
    for i in range(12):
        dates.append((start_date + timedelta(days=i*30)).strftime('%Y-%m'))
    
    # Follower data
    follower_data = {
        'dates': dates,
        'followers': [1000 + i*50 + random.randint(-20, 20) for i in range(12)]
    }
    
    # Location data
    locations = ['United States', 'United Kingdom', 'Canada', 'Australia', 'Germany']
    location_data = {
        'locations': locations,
        'followers': [random.randint(100, 500) for _ in locations],
        'views': [random.randint(1000, 5000) for _ in locations]
    }
    
    # Job function data
    job_functions = ['Marketing', 'Sales', 'Engineering', 'HR', 'Finance']
    job_data = {
        'functions': job_functions,
        'followers': [random.randint(50, 300) for _ in job_functions],
        'views': [random.randint(500, 2500) for _ in job_functions]
    }
    
    # Industry data
    industries = ['Technology', 'Healthcare', 'Finance', 'Education', 'Manufacturing']
    industry_data = {
        'industries': industries,
        'followers': [random.randint(80, 400) for _ in industries],
        'views': [random.randint(800, 4000) for _ in industries]
    }
    
    # Posting frequency data
    posting_data = {
        'months': dates,
        'post_counts': [random.randint(5, 15) for _ in dates]
    }
    
    return {
        'follower_data': follower_data,
        'location_data': location_data,
        'job_data': job_data,
        'industry_data': industry_data,
        'posting_data': posting_data
    }

def create_pie_chart(names, values):
    """Create pie chart data"""
    if not names or not values:
        return None
    
    try:
        fig = px.pie(values=values, names=names)
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    except Exception as e:
        print(f"Error creating pie chart: {e}")
        return None

@app.route('/')
def index():
    """Main page with default information"""
    try:
        data = generate_demo_data()
        
        # Create follower count chart
        follower_fig = go.Figure()
        follower_fig.add_trace(go.Scatter(
            x=data['follower_data']['dates'], 
            y=data['follower_data']['followers'], 
            name='Follower Count',
            line=dict(color='#0066cc', width=3),
            mode='lines+markers'
        ))
        follower_fig.update_layout(
            title='LinkedIn Followers Over Time',
            xaxis_title='Month',
            yaxis_title='Followers',
            template='plotly_white'
        )
        follower_chart = json.dumps(follower_fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Create posting frequency chart
        frequency_fig = go.Figure()
        frequency_fig.add_trace(go.Scatter(
            x=data['posting_data']['months'], 
            y=data['posting_data']['post_counts'], 
            name='Post Frequency',
            line=dict(color='#28a745', width=3),
            mode='lines+markers'
        ))
        frequency_fig.update_layout(
            title='Posting Frequency Over Time',
            xaxis_title='Month',
            yaxis_title='Number of Posts',
            template='plotly_white'
        )
        frequency_chart = json.dumps(frequency_fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Prepare frequency data for table
        frequency_data = dict(zip(data['posting_data']['months'], data['posting_data']['post_counts']))
        
        # Prepare data for demographics
        demographics_data = {
            'locations': data['location_data']['locations'],
            'locations_view': data['location_data']['locations'],
            'job_functions': data['job_data']['functions'],
            'job_views': data['job_data']['functions'],
            'industries': data['industry_data']['industries'],
            'industry_views': data['industry_data']['industries'],
        }
        
        # Create data tables
        location_table_data = [
            {
                'Location': loc, 
                'Total followers': fol, 
                'Location View': loc, 
                'Total views': view
            } 
            for loc, fol, view in zip(
                data['location_data']['locations'],
                data['location_data']['followers'],
                data['location_data']['views']
            )
        ]
        
        job_table_data = [
            {
                'Job function': func, 
                'Total followers': fol, 
                'Job View': func, 
                'Total views': view
            } 
            for func, fol, view in zip(
                data['job_data']['functions'],
                data['job_data']['followers'],
                data['job_data']['views']
            )
        ]
        
        industry_table_data = [
            {
                'Industry': ind, 
                'Total followers': fol, 
                'Industry View': ind, 
                'Total views': view
            } 
            for ind, fol, view in zip(
                data['industry_data']['industries'],
                data['industry_data']['followers'],
                data['industry_data']['views']
            )
        ]
        
        return render_template('index.html', 
                             follower_chart=follower_chart,
                             frequency_chart=frequency_chart,
                             frequency_data=frequency_data,
                             demographics=demographics_data,
                             location_data=location_table_data,
                             job_function_data=job_table_data,
                             industry_data=industry_table_data)
                             
    except Exception as e:
        return render_template('error.html', message=f"Error loading demo data: {str(e)}")

@app.route('/filtered')
def filtered():
    """Filtered data page"""
    try:
        # Generate some demo filter options
        filter_options = {
            'years': ['2023', '2024'],
            'months': ['Jan 2024', 'Feb 2024', 'Mar 2024', 'Apr 2024'],
            'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
            'times': ['Morning', 'Afternoon', 'Evening'],
            'categories': ['Technology', 'Business', 'Marketing', 'Education'],
            'sub_categories': ['AI/ML', 'Web Dev', 'Data Science', 'Cloud'],
            'emojis': ['💼', '🚀', '💡', '📈', '🎯'],
            'aggregates': ['Impressions', 'Clicks', 'Click through rate (CTR)', 'Engagement rate']
        }
        
        return render_template('filtered.html', 
                             filter_options=filter_options,
                             start_date='2024-01-01',
                             end_date='2024-12-31')
                             
    except Exception as e:
        return render_template('error.html', message=f"Error loading filtered page: {str(e)}")

@app.route('/api/demographics/<chart_type>')
def api_demographics(chart_type):
    """API endpoint for demographics charts"""
    try:
        selected_items = request.args.getlist('items')
        
        if not selected_items:
            return jsonify({'error': 'No items selected'})
        
        # Generate demo data based on chart type
        if 'location' in chart_type:
            values = [random.randint(100, 500) for _ in selected_items]
        elif 'job' in chart_type:
            values = [random.randint(50, 300) for _ in selected_items]
        elif 'industry' in chart_type:
            values = [random.randint(80, 400) for _ in selected_items]
        else:
            values = [random.randint(10, 100) for _ in selected_items]
        
        chart_json = create_pie_chart(selected_items, values)
        return jsonify({'chart': chart_json})
        
    except Exception as e:
        return jsonify({'error': f'Error creating chart: {str(e)}'})

@app.route('/api/filtered_chart')
def api_filtered_chart():
    """API endpoint for filtered charts"""
    try:
        # Get filter parameters
        aggregates = request.args.getlist('aggregates')
        chart_category = request.args.get('chart_category')
        
        if not aggregates or not chart_category:
            return jsonify({'error': 'Missing required parameters'})
        
        # Generate demo data
        categories = ['Category A', 'Category B', 'Category C', 'Category D']
        
        charts = {}
        tables = {}
        
        for aggregate in aggregates:
            # Generate demo values based on aggregate type
            if aggregate in ['Impressions', 'Clicks']:
                values = [random.randint(1000, 5000) for _ in categories]
            else:  # CTR, Engagement rate
                values = [round(random.uniform(1.0, 10.0), 2) for _ in categories]
            
            post_counts = [random.randint(5, 20) for _ in categories]
            
            # Create bar chart
            fig = px.bar(
                x=categories, 
                y=values, 
                title=f'{chart_category} {aggregate} Chart',
                labels={'x': chart_category, 'y': aggregate},
                color=categories,
                template='plotly_white'
            )
            
            chart_key = f"{chart_category}_{aggregate}"
            charts[chart_key] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            
            # Create table data
            tables[chart_key] = {
                chart_category: categories,
                'Number of Posts': post_counts,
                aggregate: values
            }
        
        return jsonify({'charts': charts, 'tables': tables})
        
    except Exception as e:
        return jsonify({'error': f'Error creating filtered charts: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
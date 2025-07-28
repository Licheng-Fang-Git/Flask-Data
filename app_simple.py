from flask import Flask, render_template, request, jsonify
import plotly.graph_objects as go
import plotly.utils
import json
from datetime import datetime, timedelta
import random

app = Flask(__name__)

def create_demo_line_chart(x_data, y_data, title, color='#0066cc'):
    """Create a line chart using plotly.graph_objects"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_data,
        y=y_data,
        mode='lines+markers',
        line=dict(color=color, width=3),
        marker=dict(size=8)
    ))
    fig.update_layout(
        title=title,
        template='plotly_white',
        height=400
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_demo_pie_chart(labels, values, title):
    """Create a pie chart using plotly.graph_objects"""
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(
        title=title,
        template='plotly_white',
        height=400
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_demo_bar_chart(x_data, y_data, title):
    """Create a bar chart using plotly.graph_objects"""
    fig = go.Figure(data=[go.Bar(x=x_data, y=y_data)])
    fig.update_layout(
        title=title,
        template='plotly_white',
        height=400
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/')
def index():
    """Main page with default information"""
    try:
        # Generate demo data
        months = ['Jan 2024', 'Feb 2024', 'Mar 2024', 'Apr 2024', 'May 2024', 'Jun 2024']
        followers = [1000, 1050, 1120, 1180, 1250, 1300]
        posts = [8, 12, 10, 15, 11, 9]
        
        # Create charts
        follower_chart = create_demo_line_chart(months, followers, 'LinkedIn Followers Over Time')
        frequency_chart = create_demo_line_chart(months, posts, 'Posting Frequency Over Time', '#28a745')
        
        # Demo demographics data
        locations = ['United States', 'United Kingdom', 'Canada', 'Australia', 'Germany']
        job_functions = ['Marketing', 'Sales', 'Engineering', 'HR', 'Finance']
        industries = ['Technology', 'Healthcare', 'Finance', 'Education', 'Manufacturing']
        
        demographics_data = {
            'locations': locations,
            'locations_view': locations,
            'job_functions': job_functions,
            'job_views': job_functions,
            'industries': industries,
            'industry_views': industries,
        }
        
        # Demo table data
        location_data = [
            {'Location': loc, 'Total followers': random.randint(100, 500), 
             'Location View': loc, 'Total views': random.randint(1000, 5000)}
            for loc in locations
        ]
        
        job_function_data = [
            {'Job function': func, 'Total followers': random.randint(50, 300),
             'Job View': func, 'Total views': random.randint(500, 2500)}
            for func in job_functions
        ]
        
        industry_data = [
            {'Industry': ind, 'Total followers': random.randint(80, 400),
             'Industry View': ind, 'Total views': random.randint(800, 4000)}
            for ind in industries
        ]
        
        frequency_data = dict(zip(months, posts))
        
        return render_template('index.html', 
                             follower_chart=follower_chart,
                             frequency_chart=frequency_chart,
                             frequency_data=frequency_data,
                             demographics=demographics_data,
                             location_data=location_data,
                             job_function_data=job_function_data,
                             industry_data=industry_data)
                             
    except Exception as e:
        return render_template('error.html', message=f"Error loading demo data: {str(e)}")

@app.route('/filtered')
def filtered():
    """Filtered data page"""
    try:
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
        
        # Generate demo values
        values = [random.randint(50, 500) for _ in selected_items]
        chart_json = create_demo_pie_chart(selected_items, values, f'Demographics: {chart_type}')
        
        return jsonify({'chart': chart_json})
        
    except Exception as e:
        return jsonify({'error': f'Error creating chart: {str(e)}'})

@app.route('/api/filtered_chart')
def api_filtered_chart():
    """API endpoint for filtered charts"""
    try:
        aggregates = request.args.getlist('aggregates')
        chart_category = request.args.get('chart_category')
        
        if not aggregates or not chart_category:
            return jsonify({'error': 'Missing required parameters'})
        
        # Demo categories
        categories = ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024']
        
        charts = {}
        tables = {}
        
        for aggregate in aggregates:
            if aggregate in ['Impressions', 'Clicks']:
                values = [random.randint(1000, 5000) for _ in categories]
            else:
                values = [round(random.uniform(1.0, 10.0), 2) for _ in categories]
            
            post_counts = [random.randint(5, 20) for _ in categories]
            
            chart_json = create_demo_bar_chart(categories, values, f'{chart_category} {aggregate}')
            
            chart_key = f"{chart_category}_{aggregate}"
            charts[chart_key] = chart_json
            
            tables[chart_key] = {
                chart_category: categories,
                'Number of Posts': post_counts,
                aggregate: values
            }
        
        return jsonify({'charts': charts, 'tables': tables})
        
    except Exception as e:
        return jsonify({'error': f'Error creating filtered charts: {str(e)}'})

@app.route('/health')
def health():
    """Simple health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'LinkedIn Analytics Flask App is running!'})

if __name__ == '__main__':
    print("🚀 Starting LinkedIn Analytics Flask App...")
    print("📊 Demo mode - using generated sample data")
    print("🌐 App will be available at: http://localhost:5000")
    print("📈 Features available:")
    print("   • Default Information Dashboard")
    print("   • Interactive Demographics Charts") 
    print("   • Filtered Data Analytics")
    print("   • Modern Bootstrap UI")
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5000)
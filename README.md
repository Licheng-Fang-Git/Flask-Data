# LinkedIn Analytics Flask App

A web application for analyzing LinkedIn data with interactive charts and filtering capabilities. This Flask app converts the original Streamlit application to provide a more customizable web interface.

## Features

- **Default Information Dashboard**: View total followers, demographics, and posting frequency
- **Filtered Data Analytics**: Apply multiple filters to analyze specific data segments
- **Interactive Charts**: Plotly-powered visualizations with responsive design
- **Demographics Analysis**: Pie charts for location, job function, and industry data
- **Modern UI**: Bootstrap-based responsive interface

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask application:**
   ```bash
   python app.py
   ```

4. **Open your web browser and navigate to:**
   ```
   http://localhost:5000
   ```

## Dependencies

- Flask 2.3.3
- pandas 2.1.3
- plotly 5.17.0
- numpy 1.25.2
- Werkzeug 2.3.7

## Data Source

The application connects to Google Sheets to fetch LinkedIn analytics data. The data includes:

- Content analytics from different sheets
- Follower demographics
- Location-based analytics
- Job function analytics
- Industry analytics

## Usage

### Default Information Page

- View total follower trends over time
- Explore demographic breakdowns by location, job function, and industry
- Analyze posting frequency patterns
- Interactive pie charts for demographic data

### Filtered Data Page

1. **Set Date Range**: Choose start and end dates for analysis
2. **Apply Filters**: Select from various filter options:
   - Year
   - Month & Year
   - Day of the week
   - Time intervals
   - Content categories
   - Sub-categories
   - Emoji types
3. **Choose Metrics**: Select aggregation metrics (Impressions, Clicks, CTR, Engagement rate)
4. **Select Chart Category**: Choose the dimension for chart generation
5. **Generate Charts**: Click to create interactive visualizations

## API Endpoints

- `/` - Main dashboard page
- `/filtered` - Filtered data analysis page
- `/api/demographics/<chart_type>` - Demographics chart data
- `/api/filtered_chart` - Filtered chart data

## File Structure

```
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Default information page
│   ├── filtered.html     # Filtered data page
│   └── error.html        # Error page
└── static/               # Static files
    ├── css/
    │   └── style.css     # Custom styles
    └── js/
        └── app.js        # JavaScript utilities
```

## Configuration

The Google Sheets configuration is set at the top of `app.py`. Update the following variables if needed:

```python
sheet_id = '1thMQ4ndtgzyEM6qfoA2tfrt3MEzZY2CtxhjpCTNcS0U'
content_sheet_name = 'Content'
follower_sheet = 'Sheet24'
location_sheet = 'Sheet25'
job_function_sheet = 'Sheet26'
industry_sheet = 'Sheet27'
```

## Troubleshooting

1. **Data Loading Issues**: Ensure the Google Sheets are publicly accessible or properly configured
2. **Chart Not Displaying**: Check browser console for JavaScript errors
3. **Slow Performance**: Consider implementing data caching for large datasets

## Differences from Streamlit Version

- **Navigation**: Tab-based navigation replaced with separate pages
- **Interactivity**: AJAX-based chart updates instead of full page reloads
- **Styling**: Bootstrap-based responsive design
- **Deployment**: Standard web server deployment instead of Streamlit server

## Development

To modify the application:

1. **Backend Changes**: Edit `app.py` for data processing and API endpoints
2. **Frontend Changes**: Modify HTML templates in `templates/` directory
3. **Styling**: Update `static/css/style.css` for visual changes
4. **JavaScript**: Add functionality in `static/js/app.js`

## Production Deployment

For production deployment, consider:

1. Using a production WSGI server (e.g., Gunicorn)
2. Setting up environment variables for configuration
3. Implementing data caching (Redis/Memcached)
4. Adding authentication if needed
5. Using a reverse proxy (Nginx) for static files

## License

This project is provided as-is for educational and business purposes.
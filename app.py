from flask import Flask, request, jsonify
from pytrends.request import TrendReq
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return "Google Trends API is running!"

@app.route('/trends', methods=['POST'])
def get_trends():
    try:
        # Get data from request
        data = request.get_json()
        keywords = data.get('keywords', ['AI'])
        timeframe = data.get('timeframe', 'today 3-m')  # default last 3 months
        
        # Initialize pytrends
        pytrends = TrendReq(hl='en-US', tz=360)
        
        # Build payload
        pytrends.build_payload(keywords, cat=0, timeframe=timeframe, geo='', gprop='')
        
        # Get interest over time
        interest_data = pytrends.interest_over_time()
        
        # Convert to JSON-friendly format
        if not interest_data.empty:
            # Remove 'isPartial' column if exists
            if 'isPartial' in interest_data.columns:
                interest_data = interest_data.drop('isPartial', axis=1)
            
            result = interest_data.reset_index().to_dict('records')
            return jsonify({
                'success': True,
                'data': result
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No data found'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/related-queries', methods=['POST'])
def get_related_queries():
    try:
        data = request.get_json()
        keywords = data.get('keywords', ['AI'])
        
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload(keywords, cat=0, timeframe='today 3-m')
        
        # Get related queries
        related = pytrends.related_queries()
        
        return jsonify({
            'success': True,
            'data': related
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/trending', methods=['GET'])
def get_trending():
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        
        # Get trending searches (US by default)
        trending = pytrends.trending_searches(pn='united_states')
        
        return jsonify({
            'success': True,
            'data': trending[0].tolist()  # Convert to list
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# Simple sentiment analysis using keyword matching
POSITIVE_WORDS = [
    'excellent', 'amazing', 'fantastic', 'great', 'wonderful', 'awesome', 
    'outstanding', 'superb', 'brilliant', 'perfect', 'love', 'best', 
    'good', 'nice', 'happy', 'satisfied', 'pleased', 'recommend', 
    'professional', 'friendly', 'helpful', 'quality', 'fast', 'efficient'
]

NEGATIVE_WORDS = [
    'terrible', 'awful', 'horrible', 'bad', 'worst', 'hate', 'disappointed',
    'poor', 'slow', 'rude', 'unprofessional', 'expensive', 'overpriced',
    'broken', 'defective', 'problem', 'issue', 'complaint', 'unsatisfied',
    'angry', 'frustrated', 'waste', 'regret', 'never', 'avoid'
]

def analyze_sentiment(text):
    """
    Analyze sentiment of text using simple keyword matching
    Returns: 'positive', 'negative', or 'neutral'
    """
    if not text:
        return 'neutral'
    
    # Convert to lowercase and remove punctuation
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    words = text.split()
    
    positive_score = sum(1 for word in words if word in POSITIVE_WORDS)
    negative_score = sum(1 for word in words if word in NEGATIVE_WORDS)
    
    if positive_score > negative_score:
        return 'positive'
    elif negative_score > positive_score:
        return 'negative'
    else:
        return 'neutral'

@app.route('/analyzereview', methods=['POST'])
def analyze_review():
    """
    Analyze sentiment of a review
    Expected JSON: {"review": "text to analyze"}
    Returns: {"sentiment": "positive/negative/neutral"}
    """
    try:
        data = request.get_json()
        
        if not data or 'review' not in data:
            return jsonify({'error': 'Review text is required'}), 400
        
        review_text = data['review']
        sentiment = analyze_sentiment(review_text)
        
        return jsonify({
            'sentiment': sentiment,
            'review': review_text
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'sentiment-analyzer'})

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with service information"""
    return jsonify({
        'service': 'Sentiment Analysis Microservice',
        'version': '1.0.0',
        'endpoints': {
            '/analyzereview': 'POST - Analyze sentiment of review text',
            '/health': 'GET - Health check'
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
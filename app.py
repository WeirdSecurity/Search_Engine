from flask import Flask, request, jsonify
from Inverted_Indexing import NLTKInvertedIndex
import os
app = Flask(__name__)

# Load the index into memory when the server starts
index = NLTKInvertedIndex()
index.load_index()

@app.route('/')
def home():
    return "Welcome to the WeirdSecurity Search Engine API! Use /search?q=your_query"

@app.route('/search', methods=['GET'])
def do_search():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "No query provided"}), 400
        
    results = index.search(query)
    
    # Format the results to return as JSON
    response_data = []
    for url, score in results[:10]: # Top 10 results
        meta = index.metadata.get(url, {})
        response_data.append({
            "url": url,
            "score": score,
            "title": meta.get('title', 'No Title'),
            "snippet": meta.get('snippet', 'No description available.')
        })
        
    return jsonify({"query": query, "results": response_data})

if __name__ == '__main__':
    # Grab the port from Coolify, defaulting to 8080 if not set
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

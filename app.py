from flask import Flask, render_template, request, jsonify, send_from_directory
from serpapi import GoogleSearch
import os
from export_utils import export_to_csv, export_to_json

app = Flask(__name__, static_folder='static')

# API key provided by the user
API_KEY = "f172d98da4d8c149b0c56adffb6fad2aefe3892c57c715aed85f45383eeb2e41"

def search_google(keyword, api_key, num_results=10, device="desktop", country="us"):
    """
    Search Google using SerpAPI and return the top results
    
    Args:
        keyword (str): The search query
        api_key (str): SerpAPI API key
        num_results (int): Number of results to return
        device (str): Device type (desktop, mobile, tablet)
        country (str): Country code for localized results
        
    Returns:
        list: List of dictionaries containing title and link for each result
    """
    params = {
        "engine": "google",
        "q": keyword,
        "api_key": api_key,
        "num": num_results,
        "device": device,
        "gl": country,  # Country parameter for Google search
    }
    
    # Add device-specific parameters
    if device == "mobile":
        params["device"] = "mobile"
        params["mobile"] = "1"
    elif device == "tablet":
        params["device"] = "tablet"
        params["tablet"] = "1"
    
    search = GoogleSearch(params)
    results = search.get_dict()
    
    # Check if organic results exist
    if "organic_results" not in results:
        return []
    
    # Extract titles and links from organic results
    search_results = []
    for i, result in enumerate(results["organic_results"][:int(num_results)], 1):
        title = result.get("title", "No title")
        link = result.get("link", "No link")
        search_results.append({
            "position": i,
            "title": title,
            "link": link
        })
    
    return search_results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form.get('keyword', '')
    num_results = request.form.get('num_results', '10')
    device = request.form.get('device', 'desktop')
    country = request.form.get('country', 'us')
    
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400
    
    results = search_google(
        keyword=keyword, 
        api_key=API_KEY, 
        num_results=num_results,
        device=device,
        country=country
    )
    
    return jsonify({
        "keyword": keyword,
        "num_results": num_results,
        "device": device,
        "country": country,
        "results": results
    })

@app.route('/export-to-csv', methods=['POST'])
def export_csv():
    data = request.json
    
    if not data or 'results' not in data:
        return jsonify({"error": "No results to export"}), 400
    
    results = data.get('results', [])
    keyword = data.get('keyword', 'unknown')
    num_results = data.get('num_results', '10')
    device = data.get('device', 'desktop')
    country = data.get('country', 'us')
    
    # Export results to CSV
    filename = export_to_csv(results, keyword, num_results, device, country)
    
    if filename:
        return jsonify({
            "file_name": filename,
            "file_url": f"/static/{filename}"
        })
    else:
        return jsonify({"error": "Failed to create CSV file"}), 500

@app.route('/export-to-json', methods=['POST'])
def export_json():
    data = request.json
    
    if not data or 'results' not in data:
        return jsonify({"error": "No results to export"}), 400
    
    results = data.get('results', [])
    keyword = data.get('keyword', 'unknown')
    num_results = data.get('num_results', '10')
    device = data.get('device', 'desktop')
    country = data.get('country', 'us')
    
    # Export results to JSON
    filename = export_to_json(results, keyword, num_results, device, country)
    
    if filename:
        return jsonify({
            "file_name": filename,
            "file_url": f"/static/{filename}"
        })
    else:
        return jsonify({"error": "Failed to create JSON file"}), 500

if __name__ == '__main__':
    # Make sure templates and static directories exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # For development only
    # app.run(host='0.0.0.0', port=5000, debug=True)
    
    # For production
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

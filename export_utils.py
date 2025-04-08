import csv
import os
import datetime
import json

def export_to_csv(results, keyword, num_results, device, country):
    """
    Export search results to a CSV file
    
    Args:
        results (list): List of dictionaries containing search results
        keyword (str): The search query
        num_results (int): Number of results requested
        device (str): Device type used for search
        country (str): Country code used for search
        
    Returns:
        str: Path to the created CSV file
    """
    try:
        # Create a filename based on the keyword and timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        safe_keyword = keyword.replace(' ', '_').replace('/', '_').replace('\\', '_')
        filename = f"search_results_{safe_keyword}_{timestamp}.csv"
        filepath = os.path.join('static', filename)
        
        # Ensure static directory exists
        os.makedirs('static', exist_ok=True)
        
        # Write the results to a CSV file
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            # Write header with search information
            csvfile.write(f"Google Search Results for: {keyword}\n")
            csvfile.write(f"Search Parameters: {num_results} results, {device} view, country: {country}\n")
            csvfile.write(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Create CSV writer and write column headers
            writer = csv.writer(csvfile)
            writer.writerow(["Position", "Title", "URL"])
            
            # Write data rows
            for result in results:
                writer.writerow([result['position'], result['title'], result['link']])
        
        return filename
    
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        return None

def export_to_json(results, keyword, num_results, device, country):
    """
    Export search results to a JSON file
    
    Args:
        results (list): List of dictionaries containing search results
        keyword (str): The search query
        num_results (int): Number of results requested
        device (str): Device type used for search
        country (str): Country code used for search
        
    Returns:
        str: Path to the created JSON file
    """
    try:
        # Create a filename based on the keyword and timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        safe_keyword = keyword.replace(' ', '_').replace('/', '_').replace('\\', '_')
        filename = f"search_results_{safe_keyword}_{timestamp}.json"
        filepath = os.path.join('static', filename)
        
        # Ensure static directory exists
        os.makedirs('static', exist_ok=True)
        
        # Create a data structure with all information
        data = {
            "search_info": {
                "keyword": keyword,
                "num_results": num_results,
                "device": device,
                "country": country,
                "generated_on": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            "results": results
        }
        
        # Write the results to a JSON file
        with open(filepath, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2)
        
        return filename
    
    except Exception as e:
        print(f"Error exporting to JSON: {e}")
        return None

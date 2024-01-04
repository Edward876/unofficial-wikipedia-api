import requests
from bs4 import BeautifulSoup
from flask import Flask,request,jsonify
import urllib.parse  # Import urllib.parse for unquoting URL-encoded strings
app = Flask(__name__)
url_encoding_dict = {
    '%27': "'",  # Single quote
    '%20': ' ',  # Space
    '%21': '!',  # Exclamation mark
    '%23': '#',  # Hash/Pound
    '%24': '$',  # Dollar sign
}

def decode_url(encoded_text):
    # Use urllib.parse.unquote to decode the entire URL
    decoded_text = urllib.parse.unquote(encoded_text)
    return decoded_text

def replace_encoded_text(input_string):
    decoded_string = decode_url(input_string)
    return decoded_string

def wiki(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = soup.find_all("p")
    res = ""
    for paragraph in paragraphs:
        res += paragraph.get_text()
    return res
def wiki_link(query):
    google_wiki = f"https://www.google.com/search?q=wikipedia+{query}"
    response = requests.get(google_wiki)
    soup = BeautifulSoup(response.text, "html.parser")
    wikipedia_links = [a['href'] for a in soup.find_all('a', href=True) if 'https' in a['href'] and 'wikipedia' in a['href']]
    raw_link = wikipedia_links[1]
    string_to_remove = "/url?q="
    result_string = raw_link.replace(string_to_remove, "").split("&sa")
    return replace_encoded_text(result_string[0])

@app.route("/api/wiki", methods=["GET"])
def get_wiki():
    query = request.args.get('q', '')
    if query:
        result = {"query": query, "result": wiki(wiki_link(query))}
        return jsonify(result)
    else:
     return jsonify({'error': 'No query parameter provided.'})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
    

from flask import Flask, request, jsonify
from chroma_utils import init_chroma, add_documents, search_documents

app = Flask(__name__)
collection = init_chroma("anime_embeddings")

@app.route("/")
def home():
    return "Chroma API is live 🚀"

@app.route("/add", methods=["POST"])
def add():
    try:
        data = request.json
        if not data or not isinstance(data, list):
            return jsonify({"error": "Request body must be an array of anime entries"}), 400

        add_documents(collection, data)
        return jsonify({"status": "ok", "added": len(data)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/search", methods=["POST"])
def search():
    try:
        data = request.json
        query = data.get("query")
        k = data.get("k", 5)

        if not query:
            return jsonify({"error": "Missing 'query' field"}), 400

        results = search_documents(collection, query, k)
        return jsonify({"results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)


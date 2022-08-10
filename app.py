from flask import Flask, request, jsonify

from services.services import WebServiceImpl

app = Flask(__name__)

web_service = WebServiceImpl.instance()


@app.route("/ner/related", methods=["GET"])
def get_related_ner_category():
    """ Used by autocomplete function

    sample request
    ```
    curl -X GET \
      'http://localhost:5002/ner/related?query=l' \
      -H 'cache-control: no-cache' \
      -H 'postman-token: 5eee6801-7f89-0f2a-8656-e859ed5ae926'
    ```

    sample response
    ```
    {
        "data": [
            "CARDINAL",
            "LAW",
            "LOC",
            "ORDINAL"
        ]
    }
    ```
    """
    search_term = request.args.get("query")
    related_ner_categories = web_service.retrieve_related_ner_categories(search_term=search_term)
    return jsonify(dict(data=related_ner_categories))


@app.route("/documents/search", methods=["POST"])
def get_related_document_by_ner_category():
    request_payload = request.get_json()
    ner_category = request_payload.get("ner_category")

    if len(ner_category) == 0:
        return jsonify(dict(data=[]))

    related_documents = web_service.retrieve_related_documents(ner_category)
    return jsonify(dict(data=[{"id": doc.id, "text": doc.text} for doc in related_documents]))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)

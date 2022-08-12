import flask
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from services.services import WebServiceImpl

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

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
    response = jsonify(dict(data=related_ner_categories))
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route("/documents/search", methods=["POST", "OPTIONS"])
@cross_origin(origin='*')
def get_related_document_by_ner_category():
    if request.method == "OPTIONS":
        response = flask.Response()
        return response

    request_payload = request.get_json()
    ner_category = request_payload.get("ner_category")

    if len(ner_category) == 0:
        response = jsonify(dict(data=[]))
        return response

    related_documents = web_service.retrieve_related_documents(ner_category)
    response = jsonify(dict(data=[{"id": doc.id, "text": doc.text} for doc in related_documents]))
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)

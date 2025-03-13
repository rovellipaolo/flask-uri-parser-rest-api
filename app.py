import tomllib
from flask import Flask, jsonify, request
from flasgger import Swagger
from uri_parser.uri_parser import UriParser

app = Flask(__name__)
app.config.from_file("config.toml", load=tomllib.load, text=False)
app.logger.setLevel(app.config['LOG_LEVEL'])
with app.app_context():
    app.logger.debug("Loading...")

swagger = Swagger(
    app,
    config={
        "headers": [],
        "openapi": "3.0.2",
        "specs": [{"endpoint": "openapi", "route": "/openapi.json"}],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/"
    },
    template={
        "info": {"title": "URI Parser REST API", "description": "REST API to parse URIs", "version": "1.0"}
    }
)


@app.route("/api/status", methods=["GET"])
def hello():
    """Check the status of the REST API.
    ---
    components:
      schemas:
        StatusResponse:
          type: object
          required: [message]
          properties:
            message:
              type: string
              description: The status description
        ErrorResponse:
          type: object
          required: [error, message]
          properties:
            error:
              type: string
              description: The error type, such as Bad Request or Internal Server Error
            message:
              type: string
              description: The error description
    responses:
      200:
        description: The status of the REST API
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/StatusResponse"
      500:
        description: 500 Internal Server Error response
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ErrorResponse"
    """
    return jsonify(message="REST API up and running... long live and prosper!"), 200


@app.route("/api/parse", methods=["POST"])
def parse():
    """Parse a given URI.
    ---
    parameters:
      - name: force
        in: query
        description: Whether the parsing should be forced, even if the URI is not recognized as valid
        required: false
        schema:
          type: boolean
          default: false
    requestBody:
      description: A JSON containing the URI to be parsed
      required: true
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ParseRequest"
    components:
      schemas:
        ParseRequest:
          type: object
          required: [uri]
          properties:
            uri:
              type: string
              description: The URI to be parsed
        ParseResponse:
          type: object
          required: [raw]
          properties:
            fragment:
              type: string
              description: The fragment identifier of the URI, if any
              nullable: true
            host:
              type: string
              description: The hostname of the URI, if any
              nullable: true
            port:
              type: integer
              description: The port part of the URI, if any
              nullable: true
            path:
              type: string
              description: The path part of the URI, if any
              nullable: true
            query:
              type: string
              description: The query part of the URI, if any
              nullable: true
            raw:
              type: string
              description: The raw URI as a string
            scheme:
              type: string
              description: The scheme part of the URI, if any
              nullable: true
            userinfo:
              type: string
              description: The userinfo part of the URI, if any
              nullable: true
    responses:
      200:
        description: The URI parts
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ParseResponse"
      400:
        description: 400 Bad Request response
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ErrorResponse"
      500:
        description: 500 Internal Server Error response
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ErrorResponse"
    """
    force = request.args.get("force", "false") == "true"
    body = request.get_json(force=True, silent=True)
    uri = body.get("uri") if body else None
    if not uri:
        return jsonify(error="Bad Request", message="Missing 'uri' parameter in request!"), 400

    uri_parser = UriParser(logger=app.logger)
    if not force and not uri_parser.is_valid(uri):
        return jsonify(error="Bad Request", message=f"Not a valid URI: {uri}"), 400

    info = uri_parser.parse(uri)
    return jsonify(info), 200


if __name__ == "__main__":
    app.run(debug=True)

import tomllib
from flask import Flask, jsonify, request
from uri_parser.uri_parser import UriParser

app = Flask(__name__)
app.config.from_file("config.toml", load=tomllib.load, text=False)
app.logger.setLevel(app.config['LOG_LEVEL'])
with app.app_context():
    app.logger.debug("Loading...")


@app.route("/api/status", methods=["GET"])
def hello():
    return jsonify(message="REST API up and running... long live and prosper!"), 200


@app.route("/api/parse", methods=["POST"])
def parse():
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

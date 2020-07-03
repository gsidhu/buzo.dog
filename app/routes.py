from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask import current_app as app
try:
    from . import crud
except:
    import crud

# app = Flask(__name__)
# app.config["DEBUG"] = True
# CORS(app)

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Buzo.Dog API v1</h1>
<p>A no nonsense API.</p>'''

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/api/v1/resources/links', methods=['GET'])
def api_filter():
    if request.method != 'GET':
        return make_response('Malformed request', 400)

    query_parameters = request.args
    source = query_parameters.get('source')
    count = int(query_parameters.get('count'))

    if source is None:
        result = crud.read(count=count)
    else:
        result = crud.read(count=count, source=source)

    return jsonify(result)
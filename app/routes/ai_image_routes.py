from flask_restx import Resource, fields, abort, reqparse
from flask import jsonify, request
from werkzeug.datastructures import FileStorage
from ..services.ai_service import AI_Service

upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)

def ai_routes(ai_ns):
    @ai_ns.route("/personalcolor")
    class AiTest(Resource):
        @ai_ns.expect(upload_parser)
        @ai_ns.doc(responses={
            400: "Bad request. need 'new_sentence'",
            500: "Cannot find the AI Model"
        })
        def post(self):           
            new_sentence = request.data
            try:
                personal_color, rgb = AI_Service.AI_predict(new_sentence)
            except OSError:
                abort(500, error="Cannot find the AI Model")
            return jsonify({'result': personal_color[0], 'rgb': rgb})

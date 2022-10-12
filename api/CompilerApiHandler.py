from flask_restful import Api, Resource, reqparse
from compiler import executeCompilerCode


class CompilerApiHandler(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('code', type=str)
        args = parser.parse_args()

        code = args['code']
        try:
            result = executeCompilerCode(code)
            return {"status": "Success", "code_sent": code}, 200
        except Exception as e:
            return {'message': str(e)}, 400

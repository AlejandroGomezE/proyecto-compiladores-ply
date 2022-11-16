from flask_restful import Api, Resource, reqparse
from compiler import executeCompilerCode


class CompilerApiHandler(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('code', type=str)
        args = parser.parse_args()

        code = args['code']
        try:
            result, constants_table, scopes_table, virtual_var_list = executeCompilerCode(
                code)
            return {"code_quads": result, "constants_table": constants_table, "scopes_table": scopes_table, "virtual_var_list": virtual_var_list}, 200
        except Exception as e:
            return {'message': str(e)}, 400

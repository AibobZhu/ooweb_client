from flask import make_response, request, jsonify
from flask_restful import abort, Api
from flask_httpauth import HTTPBasicAuth
import json, zlib
#TODO(haibo.zhu@hotmail.com): Check HTTPBasicAuth thread safe

APIs = {
    'render': '/api/{}/render'
}

auth = HTTPBasicAuth()


@auth.error_handler
def unauthorized():
    print(request.base_url)
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@auth.verify_password
def verify_password(username, password):
    print('username:{}, password:{}'.format(username, password))
    if username != 'haibo' or password != 'python':
        return False
    return True


def abort_if_task_doesnt_exist(task_id, tasks):
    if task_id not in tasks:
        abort(404, message="Task {} doesn't exist".format(task_id))


def create_payload(data_input, compress=True):
    if not isinstance(data_input, str):
        data_json = json.dumps(data_input)
    else:
        data_json = data_input
    print('len of data_input:{}, data_json:{}'.format(len(data_input), len(data_json)))
    if compress:
        data_bytes_com = zlib.compress(data_json.encode('utf8'))
        data_str = data_bytes_com.hex()
        print('len of compressed data:{}'.format(len(data_str)))
    else:
        data_str = data_json

    return {'data': data_str}


def extract_data(data_str_com, compressed=True):
    if compressed:
        rd_bytes_com = bytes.fromhex(data_str_com)
        rd = zlib.decompress(rd_bytes_com)
        rd = rd.decode('utf8')
    else:
        rd = data_str_com
    #rd = json.loads(rd_json)
    return rd

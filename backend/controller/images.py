
from flask import Blueprint, request, jsonify

from entity.execution import Execution
from service.image import ImageService
from util.validator import Validator

images_bp = Blueprint('images', __name__, url_prefix='/api')

# 用于保存执行记录信息的列表
execution_history = []


@images_bp.route('/get-images', methods=['GET'])
def get_images_info():
    args = request.args
    num = args.get('number', None)
    start_time = args.get('startTime', None)

    # 参数校验
    if Validator.image_input_validator(start_time, num):
        res = ImageService.get_image_by_num(int(num))
    else:
        res = {'status': 400, 'message': "Invalid input parameters!"}
    res['execution_time'] = start_time
    res['input'] = num
    execution_history.append(Execution(**res))
    return jsonify(res)


@images_bp.route('/get-records', methods=['GET'])
def get_records_info():
    return jsonify({'status': 200, 'message': execution_history[::-1]})

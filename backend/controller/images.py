import json

from flask import Blueprint, request, current_app

from service.image import ImageService

images_bp = Blueprint('images', __name__, url_prefix='/api')

# 用于保存执行记录信息的列表
execution_history = []

@images_bp.route('/get-images', methods=['GET'])
def get_images_info():
    args = request.args
    num = args.get('number', None)
    start_time = args.get('start_time', '')

    # 对num进行校验

    res = ImageService.get_image_by_num(int(num))
    return_dict = {'return_code': '200', 'result': None}
    return res


@images_bp.route('/get-records', methods=['GET'])
def get_records_info():
    params = request.get_json()

    return 20

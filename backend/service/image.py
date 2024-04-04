import requests


class ImageService:

    @staticmethod
    def get_image_by_num(num: int):
        url = "https://dog.ceo/api/breeds/image/random/{}".format(num)

        try:
            response = requests.get(url, timeout=2)
            res = response.json()
            res['status'] = 200
            return res
        except Exception as e:
            return {'status': 500, 'message': str(e)}

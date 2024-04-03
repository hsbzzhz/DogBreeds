import requests


class ImageService:

    @staticmethod
    def get_image_by_num(num: int):
        url = "https://dog.ceo/api/breeds/image/random/{}".format(num)

        try:
            response = requests.get(url, timeout=1.2)
            return response.json()
        except Exception as e:
            return {'status': 500, 'message': str(e)}

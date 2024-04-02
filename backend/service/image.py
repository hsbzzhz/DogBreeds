import requests


class ImageService:

    @staticmethod
    def get_image_by_num(num: int):
        url = "https://dog.ceo/api/breeds/image/random/{}".format(num)

        response = requests.get(url, timeout=3)

        data = response.json()
        return data


if __name__ == '__main__':
    ImageService.get_image_by_num(8)

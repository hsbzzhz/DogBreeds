class Validator:

    @staticmethod
    def image_input_validator(start_time, num) -> bool:
        if not num or not start_time:
            return False
        try:
            num = int(num)
            if not 1 <= num <= 8:
                return False
            float(start_time)

        except ValueError:
            return False
        return True

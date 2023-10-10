class Validators:

    @staticmethod
    def float_validator(val):
        valid_float = False
        result = None
        try:
            result = float(val)
            valid_float = True
        except Exception:
            pass
        return result, valid_float

    @staticmethod
    def int_validator(val):
        valid_int = False
        result = None
        try:
            result = int(val)
            valid_int = True
        except Exception:
            pass
        return result, valid_int

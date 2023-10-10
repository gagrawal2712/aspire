from cryptography.hazmat.primitives.hashes import SHA512


SECURE_HASH_ALGORITHM = SHA512
AUTH_TOKEN_CHARACTER_LENGTH = 64
TOKEN_TTL = None
TOKEN_LIMIT_PER_USER = None
AUTO_REFRESH = True
MIN_REFRESH_INTERVAL = 60
AUTH_HEADER_PREFIX = 'token'

LOGIN_REFRESH_INTERVAL = 24 * 60 * 60


class CONSTANTS:
    """

    """
    TOKEN_KEY_LENGTH = 8
    DIGEST_LENGTH = 128

    def __setattr__(self, *args, **kwargs):
        raise Exception('''
            Constant values must NEVER be changed at runtime, as they are
            integral to the structure of database tables
            ''')


CONSTANTS = CONSTANTS()

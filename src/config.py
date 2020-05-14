class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "bY\xff\x04\xady\x11i\x8e\xe3\xf5\x04\xccQ\xfb8\x9c"

    SESSION_COOKIE_SECURE = True


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True

    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    TESTING = True

    SESSION_COOKIE_SECURE = False

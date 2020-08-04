import configparser
from datetime import timedelta, datetime

cfg = configparser.ConfigParser()
cfg.read('config.cfg')

class Config():
    APP_NAME = cfg['app']['name']
    SECRET_KEY = cfg['app']['secret_key']
    MAX_LOGIN_ATTEMPT = cfg['app']['max_login_attempt']

    if cfg['mysql']['log_queries'].upper() == 'TRUE':
        LOG_QUERY = True
    else:
        LOG_QUERY = False

    MASTER_DATABASE = {
        'driver': 'mysql',
        'host': cfg['mysql']['host'],
        'database': cfg['mysql']['db'],
        'user': cfg['mysql']['user'],
        'password': cfg['mysql']['password'],
        'prefix': cfg['mysql']['prefix'],
        'log_queries': LOG_QUERY
    }
    
    ORATOR_DATABASES = {
        'default': 'master',
        'master': MASTER_DATABASE
    }

    MONGODB_HOST = cfg['mongodb']['host']
    MONGODB_PORT = int(cfg['mongodb']['port'])
    MONGODB_DB = cfg['mongodb']['db']

    MONGODB_HISTORY_HOST = cfg['mongodb_history']['host']
    MONGODB_HISTORY_PORT = int(cfg['mongodb_history']['port'])
    MONGODB_HISTORY_DB = cfg['mongodb_history']['db']

    LOG_RESOURCE_PATH = cfg['app']['log_path']

    # Blueprint config autoloader
    BLUEPRINT = {}
    fbpcf = [key for key, value in cfg.items() if 'blueprint_' in key.lower()]
    if len(fbpcf) > 0:
        for bp in fbpcf:
            for k, v in cfg[bp].items():
                kname = bp.replace('blueprint_', '').upper()
                if kname not in BLUEPRINT:
                    BLUEPRINT[kname] = {}
                BLUEPRINT[kname][k.upper()] = v


class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

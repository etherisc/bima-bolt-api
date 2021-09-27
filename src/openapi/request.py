import logging

import connexion

SERVER_HOST_ATTRIBUTE = "host"
# SERVER_PATH_ATTRIBUTE = "path"
SERVER_PATH_ATTRIBUTE = "PATH_INFO"
SERVER_PATH_PREFIX = "/api/v"

PATH_VERSION_IDX = 2
PATH_TENANT_IDX = 3

ENVIRONMENT_PRODUCTION = "production"

ERROR_HOST_MESSAGE = "host '{}' does not comply to required format <tenant>[-<environment>].<domain>"
ERROR_PATH_MESSAGE = "path '{}' does not comply to required format /api/v<version-number>/"

# setup up logging handler
logging.getLogger(__name__).addHandler(logging.NullHandler())


def validate_request_host():
    return (get_tenant(), get_environment())


def get_tenant():
    tenant_environment = _get_tenant_environment()

    if tenant_environment:
        if '-' in tenant_environment:
            tenant_candidate = tenant_environment.split('-')[0]

            if len(tenant_candidate) > 0:
                return tenant_candidate
            else:
                _host_format_panic_and_abort("tenant is missing")
        else:
            return tenant_environment
    
    return None


def get_environment():
    tenant_environment = _get_tenant_environment()

    if tenant_environment:
        if '-' in tenant_environment:
            toks = tenant_environment.split('-')[1:]
            environment_candidate = '-'.join(toks)

            if len(environment_candidate) > 0:
                if environment_candidate != ENVIRONMENT_PRODUCTION:
                    return environment_candidate
                else:
                    _host_format_panic_and_abort("environment 'production' must be specified by omitting environment information in the host string")
            else:
                _host_format_panic_and_abort("empty environment after '-'")
        else:
            return ENVIRONMENT_PRODUCTION
    
    return None


def get_api_version():
    path = _get_path()

    logging.info("get_api_version path {}".format(path))

    if path.startswith(SERVER_PATH_PREFIX):
        version_candidate = path.split('/')[PATH_VERSION_IDX]
        number_candidate = version_candidate[1:]

        try:
            number = int(number_candidate)
        except:
            _path_format_panic_and_abort()

        return version_candidate

    return None


def _get_tenant_environment():
    path = _get_path()

    if path and '/' in path:
        return path.split('/')[PATH_TENANT_IDX]
        
    return None


def _host_format_panic_and_abort(detail):
    reason = ERROR_HOST_MESSAGE.format(_get_host())
    message = "PANIC AND ABORT REQUEST {}. {}".format(reason, detail)
    logging.error(message)
    raise HostPathError(message)


def _path_format_panic_and_abort():
    reason = ERROR_PATH_MESSAGE.format(_get_path())
    message = "PANIC AND ABORT REQUEST {}".format(reason)
    logging.error(message)
    raise HostPathError(message)


def _get_host():
    rd = connexion.request.__dict__
    
    if SERVER_HOST_ATTRIBUTE in rd.keys():
        return rd[SERVER_HOST_ATTRIBUTE]
    
    return None


def _get_path():
    rd = connexion.request.__dict__
    environ = 'environ'

    if environ in rd:
        env = rd[environ]

        if SERVER_PATH_ATTRIBUTE in env:
            return env[SERVER_PATH_ATTRIBUTE]
        
        else:
            logging.warning("{} expected but not found in {}".format(SERVER_PATH_ATTRIBUTE, env))
    
    if SERVER_PATH_ATTRIBUTE in rd.keys():
        return rd[SERVER_PATH_ATTRIBUTE]

    else:
        logging.warning("{} expected but not found in {}".format(SERVER_PATH_ATTRIBUTE, rd))

    return None


class HostPathError(Exception):

    def __init__(self, value): 
        self.value = value
    
    def __str__(self): 
        return "Error: {}".format(self.value)

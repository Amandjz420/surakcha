VERSION = (0, 1, 0)


def get_short_version():
    return '%s.%s' % (VERSION[0], VERSION[1])


def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    # Append 3rd digit if > 0
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    return version

try:
    from base_schema import *
except:
    pass

try:
    from base_views import *
except:
    pass

try:
    from exceptions import *
except:
    pass

try:
    from exception_handler import *
except:
    pass

try:
    from fields import *
except:
    pass

try:
    from utils import *
except:
    pass
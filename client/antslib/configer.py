"""configer
====================

Handle parsing of configuraiton file options.
"""


import ConfigParser
import os
import pwd
import grp


def is_root():
    """Check if user is root and return True or False."""
    if os.geteuid() == 0:
        return True
    return False


def create_dir(dir_name, user='root', group='wheel'):
    """Create directory

    Use pwd and grp to get uid/gid.
    https://stackoverflow.com/questions/5994840/how-to-change-the-user-and-group-permissions-for-a-directory-by-name
    """
    uid = pwd.getpwnam(user).pw_uid
    gid = grp.getgrnam(group).gr_gid
    os.mkdir(dir_name, 0755)
    os.chown(dir_name, uid, gid)


def read_config(config_section, config_file='ants.cfg'):
    """Read indicated configuraton section and return a dict.

    Uses config.optionxform to preserver upper/lower case letters
    in config file.
    """

    ants_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    default_config = os.path.join(ants_path, 'etc', config_file)
    config_path = '/etc/ants/'
    system_config = os.path.join(config_path, config_file)

    if not os.path.isfile(default_config):
        raise OSError('Default config file not found at %s' % default_config)

    config = ConfigParser.ConfigParser()
    config.optionxform = str
    config.read([default_config, system_config])

    return dict(config.items(config_section))


def get_values(cfg):
    """Take and return a dict of values and prompt the user for a reply."""
    for key, value in cfg.iteritems():
        cfg[key] = raw_input("%s [Example: %s]:" % (key, value)) or value
    return cfg


def get_config():
    """Get configuration from command line and return ConfigParser opject

    If no value is specified by the user, the value marked as *example*
    will be written set.

    Only values that differ from the system defaults are written to
    the local config file.
    """
    cfg_main = get_values(read_config('main'))
    cfg_ad = get_values(read_config('ad'))

    config = ConfigParser.ConfigParser()
    config.add_section('main')
    for key, value in cfg_main.iteritems():
        config.set('main', key, value)
    config.add_section('ad')
    for key, value in cfg_ad.iteritems():
        config.set('ad', key, value)
    return config


def write_config(config, config_file='ants.cfg'):
    """Writing ConfigParser object to local configuration. Existing files will be overwritten."""
    config_path = '/etc/ants/'
    system_config = os.path.join(config_path, config_file)
    if not os.path.isdir(config_path):
        create_dir(config_path)
    with open(system_config, 'w') as cfg:
        config.write(cfg)


if __name__ == '__main__':
    pass

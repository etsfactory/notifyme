def field_config_file(config, section, option=None):
    if (isinstance(config, dict)):
        field = config[section]
        if isinstance(field, dict):
            return field[option]
        return config[section]
    else:
        config.get(section, option)

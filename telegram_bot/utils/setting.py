import settings

class Settings:
    def __init__(self):
        pass

for var_name in dir(settings):
    if not var_name.startswith('__') and var_name not in settings.LIST_NOT_USE_VAR:
        var_value = getattr(settings, var_name)
        if isinstance(var_value, (int, bool, float, str)):
            setattr(Settings, var_name, var_value)



settings = Settings()


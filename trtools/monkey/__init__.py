def patch(classes, name=None):
    if not isinstance(classes, list):
        classes = [classes]

    def decorator(func):
        for cls in classes:
            func_name = name and name or func.__name__
            if hasattr(cls, func_name):
                old_func = getattr(cls, func_name)
                setattr(cls, '_old_'+func_name, old_func)
            setattr(cls, func_name, func)
        return func
    return decorator

def patch_prop(classes, name=None):
    if not isinstance(classes, list):
        classes = [classes]

    def decorator(func):
        for cls in classes:
            prop_name = name and name or func.__name__
            func_name = '_func_'+prop_name        
            setattr(cls, func_name, func)
            prop = property(func)
            setattr(cls, prop_name, prop)

        return func
    return decorator

def patcher(classes, func, name=None):
    if not isinstance(classes, list):
        classes = [classes]

    for cls in classes:
        func_name = name and name or func.__name__
        if hasattr(cls, func_name):
            old_func = getattr(cls, func_name)
            setattr(cls, '_old_'+func_name, old_func)
        setattr(cls, func_name, func)
    return func

import json
from typing import List, Dict
from functools import wraps

from database.pydantic_plugin import Plugin


def get_plugins_from_db(entrypoint) -> List[Plugin]:
    result = []
    for plug_dict in json.load(open('db.json')):
        plugin = Plugin(**plug_dict)
        if plugin.entrypoint == entrypoint:
            result.append(plugin)
        return result


def compile_and_run_plugin_exe(plugin: Plugin, func_globals: dict) -> None:
    filepath = os.path.join(os.getcwd(), plugins_dirname, plugin.filename)
    with open(filepath) as f:
        compiled_plug = compile(f.read(), filepath, 'exec')
    exec(compiled_plug, func_globals)


def add_compile_plugins(func):
    """Add plugins before and after func run"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        after_func_plugins = []
        for plugin in get_plugins_from_db(func.__name__):
            if not plugin.enabled:
                continue
            if plugin.after:
                after_func_plugins.append(plugin)
            else:
                compile_and_run_plugin_exe(plugin, func.__globals__)

        result = func(*args, **kwargs)

        for plugin in after_func_plugins:
            compile_and_run_plugin_exe(plugin, func.__globals__)

        return result
    return wrapper

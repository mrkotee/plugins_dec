import json
import importlib.util
import os.path
from loguru import logger

from abc import ABC, abstractmethod
from importlib.machinery import ModuleSpec
from typing import List, Union
from types import ModuleType
from functools import wraps

from database.pydantic_plugin import Plugin
from settings import plugins_dirname


class AbstractPluginDecorator(ABC):
    """
        Import plugins (before and after func) as module
        and run plugin.before() and plugin.after() funcs

    """

    def __init__(self, use_func_args=False, use_func_result=False):
        self.use_func_args = use_func_args
        self.use_func_result = use_func_result

    @abstractmethod
    def get_plugins_from_db(self, entrypoint) -> List[Plugin]:
        raise NotImplementedError

    def get_plug_module_path(self, plugin: Plugin) -> str:
        return os.path.join(plugins_dirname, plugin.filename)

    def plugin_exist(self, plugin: Plugin) -> Union[ModuleSpec, None]:
        """Check plugin con be imported"""
        plugin_spec = importlib.util.spec_from_file_location(plugin.name, self.get_plug_module_path(plugin))
        if not plugin_spec:
            return None
        return plugin_spec

    def import_plugin(self, plugin: Plugin) -> ModuleType:
        """Import plugin from filepath"""
        spec = importlib.util.spec_from_file_location(plugin.name, self.get_plug_module_path(plugin))
        plugin_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(plugin_module)
        return plugin_module

    def run_plugin(self, plugin: Plugin, *args, after=False, func_result=None, **kwargs) -> None:
        try:
            plugin_module = self.import_plugin(plugin)
            if after:
                if hasattr(plugin_module, "after"):
                    plugin_module.after()
            else:
                if hasattr(plugin_module, "before"):
                    plugin_module.before()
        except Exception as e:
            logger.error(f"Plugin {plugin.name} not working, exception: {e}")

    def __call__(self, func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            after_func_plugins = []
            for plugin in self.get_plugins_from_db(entrypoint=func.__name__):
                if not plugin.enabled:
                    continue
                if not self.plugin_exist(plugin):
                    logger.warning(f"{plugin.name} not found")
                    continue
                if plugin.after:
                    after_func_plugins.append(plugin)
                else:
                    if self.use_func_args:
                        self.run_plugin(plugin, *args, after=False, **kwargs)
                    else:
                        self.run_plugin(plugin, after=False)

            result = func(*args, **kwargs)

            for plugin in after_func_plugins:
                plugin_kwargs = {'after': True}
                if self.use_func_args:
                    plugin_kwargs.update(kwargs)
                if self.use_func_result:
                    plugin_kwargs["func_result"] = result

                self.run_plugin(plugin, plugin_kwargs)

            return result
        return wrapper


class JSONPluginDecorator(AbstractPluginDecorator):
    """Example with JSON file as db"""

    def get_plugins_from_db(self, entrypoint) -> List[Plugin]:
        result = []
        for plug_dict in json.load(open('database/db.json')):
            plugin = Plugin(**plug_dict)
            if plugin.entrypoint == entrypoint:
                result.append(plugin)
        return result

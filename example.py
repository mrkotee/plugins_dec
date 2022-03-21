import os
import sys
# from loguru import logger

from plugs_module_decor import add_module_plugins

from database.models import User


@add_module_plugins(use_func_args=True)
def some_func():
    print("do some stuff")


class SomeClass:

    @add_module_plugins()
    def some_else_func(self):
        print("do cls staff")


some_func()

some_cls = SomeClass()
some_cls.some_else_func()

import os
import sys

from plugin_decor_class import JSONPluginDecorator

from database.models import User


@JSONPluginDecorator(use_func_args=True)
def some_func():
    print("do some stuff")


class SomeClass:

    @JSONPluginDecorator()
    def some_else_func(self, asd):
        print("do cls staff")


some_func()

some_cls = SomeClass()
print(some_cls)
some_cls.some_else_func(asd="asdf")

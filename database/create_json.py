import json
from plugins.pydantic_plugin import Plugin


some_plug = Plugin(name="some plug", filename="some_plugin.py", entrypoint="some_func", before=True, enabled=True)
some_plug2 = Plugin(name="some plug2", filename="some_plugin2.py", entrypoint="some_else_func", after=True, enabled=True)

json.dump([some_plug.dict(), some_plug2.dict()], open("db.json", 'w'))

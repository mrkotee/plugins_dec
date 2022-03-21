



for import additional modules in plugin:
```
import importlib.util

spec = importlib.util.spec_from_file_location("module.name", "path/to/module")
add_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(add_module)
```
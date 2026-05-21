from __future__ import annotations

import importlib
import pkgutil
from typing import List

from jarvis.plugins.base import Plugin


def load_plugins() -> List[Plugin]:
    plugins: list[Plugin] = []
    package_name = 'jarvis.plugins.modules'
    try:
        package = importlib.import_module(package_name)
    except ModuleNotFoundError:
        return plugins

    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f'{package_name}.{module_name}')
        plugin = getattr(module, 'plugin', None)
        if plugin is not None:
            plugins.append(plugin)
    return plugins

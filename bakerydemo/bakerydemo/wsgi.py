import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bakerydemo.settings.dev")

# --- ХАК ДЛЯ ОБХОДА БАГА DJANGO 6.0.4 FROZENINSTANCEERROR ---
try:
    import dataclasses
    from django_tasks.base import TaskResult

    # Делаем класс TaskResult изменяемым в рантайме, чтобы typing не падал
    if hasattr(TaskResult, "__dataclass_params__"):
        TaskResult.__dataclass_params__.frozen = False
    
    # Переопределяем __setattr__, чтобы он никогда не кидал FrozenInstanceError
    def loose_setattr(self, name, value):
        object.__setattr__(self, name, value)
        
    TaskResult.__setattr__ = loose_setattr
except Exception:
    pass
# -----------------------------------------------------------

application = get_wsgi_application()
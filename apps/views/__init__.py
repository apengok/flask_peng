from apps.views.auths import mod
from apps.models.auths import Permission

@mod.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)

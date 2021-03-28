"""
components/gpg/__init__.py

Init file for GPG component, provides registration function for widget integration
"""


from .gpgframe import GPGFrame 
from .gpgcontroller import GPGController
from .gpgmodel import GPGModel
name = 'GPG'


def register_widget(root, view_method, model_method,  override_name=name):
    view = view_method(GPGFrame, text=name)
    model = model_method(name, GPGModel)
    controller = GPGController(root, view, model)
    return controller

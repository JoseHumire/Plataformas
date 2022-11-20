"""
Account inputs
"""
from graphene import (
    String,
    InputObjectType,
)

from django.utils.translation import ugettext_lazy as _


class RegisterInput(InputObjectType):
    """
    Register input
    """

    email = String(required=True, description=_('Email'))
    first_name = String(required=True, description=_('First name'))
    last_name = String(required=True, description=_('Last name'))
    password1 = String(required=True, description=_('Password 1'))
    password2 = String(required=True, description=_('Password 2'))

from graphene import Mutation, Boolean, List, Field, ObjectType, String, Enum
from graphene_django.types import ErrorType

from django.utils.translation import ugettext_lazy as _


class FeedbackType(ObjectType):
    message = String(default_value=None)

    class Meta:
        message = _('Message type to return feedback information')


class BaseMutation(Mutation):
    """
    Base mutation class
    """
    class Meta:
        abstract = True

    success = Boolean(default_value=None, description=_('success'))
    feedback = Field(FeedbackType, default_value=None)
    field_errors = List(
        ErrorType,
        description=_("May contain more than one error for same field."),
        default_value=None,
    )

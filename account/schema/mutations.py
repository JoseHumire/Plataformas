"""
Account mutations
"""
import graphene
from graphene import (
    ObjectType,
    Field,
)
from graphene_django.types import ErrorType

from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.utils.http import urlsafe_base64_decode

from core.tokens import account_activation_token
from account.models import User
from account.schema.types import UserType
from account.schema.inputs import RegisterInput
from core.schema import BaseMutation, FeedbackType
from account.serializers import RegisterSerializer


class RegisterMutation(BaseMutation):
    """
    Register mutation
    """

    user = Field(UserType, description=_('User'))

    class Arguments:
        input = RegisterInput(required=True)

    def mutate(self, info, **kwargs):
        inputs = kwargs.pop('input')
        serializer = RegisterSerializer(data=inputs)

        if serializer.is_valid():
            user = serializer.save()

            return RegisterMutation(
                user=user,
                success=True,
                feedback=FeedbackType(message=_('Usuario registrado con éxito')),
            )

        return RegisterMutation(
            success=False,
            feedback=FeedbackType(message=_('No se pudo completar el registro')),
            field_errors=ErrorType.from_errors(serializer.errors)
        )


class VerifyEmailMutation(BaseMutation):
    """
    Verify Email mutation
    """
    class Arguments:
        token = graphene.String(required=True)
        uid = graphene.String(required=True)

    @staticmethod
    def mutate(root, info, token, uid):
        try:
            uid = force_text(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)

        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        valid_token = account_activation_token.check_token(user, token)
        can_activate = user is not None and valid_token

        if can_activate:
            user.is_active = True
            user.save()

            return VerifyEmailMutation(
                success=True,
                feedback=FeedbackType(message=_('Correo verificado'))
            )

        return VerifyEmailMutation(
            success=False,
            feedback=FeedbackType(message=_('No se pudo verificar el correo'))
        )


class Mutation(ObjectType):
    """
    Account mutations
    """
    register = RegisterMutation.Field(
        description=_('Register')
    )
    verify_email = VerifyEmailMutation.Field(
        description=_('Verify email')
    )

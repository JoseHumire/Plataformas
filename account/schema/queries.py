import graphene

from graphql_jwt.decorators import login_required

from account.models import User
from account.schema.types import UserType


class Query(graphene.ObjectType):
    get_users = graphene.List(UserType)
    me = graphene.Field(UserType)
    check_email_already_exists = graphene.Boolean(email=graphene.String())

    def resolve_get_users(self, info, **kwargs):
        return User.objects.all()

    @login_required
    def resolve_me(self, info):
        user = info.context.user

        return user

    def resolve_check_email_already_exists(self, info, email):
        emails = list(User.objects.values_list('email', flat=True))
        return email in emails

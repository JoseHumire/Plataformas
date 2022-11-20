import graphql_jwt
from graphene import Schema, String, ObjectType, Field
from graphql_jwt import JSONWebTokenMutation

from account.schema.queries import Query as AccountQueries
from account.schema.mutations import Mutation as AccountMutations
from account.schema.types import UserType


class ObtainJSONWebToken(JSONWebTokenMutation):
    """
    Overwrite obtain token to get user too
    """
    user = Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        """
        Return user
        :param root: root
        :param info: info
        :param kwargs: kwargs
        :return: class instance
        """
        return cls(user=info.context.user)


class Query(AccountQueries, ObjectType):
    hello = String(default_value="Hi!")


class Mutation(AccountMutations, ObjectType):
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = Schema(query=Query, mutation=Mutation)

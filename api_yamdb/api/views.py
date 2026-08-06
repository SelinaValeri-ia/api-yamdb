from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import User

from .permissions import IsAdmin
from .serializers import UserMeSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    search_fields = ('username',)
    http_method_names = [
        'get', 'post', 'patch', 'delete', 'head', 'options',
    ]

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(IsAuthenticated,),
        url_path='me',
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = UserMeSerializer(
                request.user, data=request.data, partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        serializer = UserMeSerializer(request.user)
        return Response(serializer.data)

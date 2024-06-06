from django.middleware.csrf import get_token
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Chemogene
from .serializers import ChemogeneSerializer


class ChemogeneViewSet(viewsets.ModelViewSet):
    queryset = Chemogene.objects.all()
    serializer_class = ChemogeneSerializer

    def dispatch(self, *args, **kwargs):
        # 获取请求对象
        request = args[0]
        # 强制生成新的 CSRF 令牌
        get_token(request)
        # 调用父类的 dispatch 方法
        response = super().dispatch(*args, **kwargs)
        # 将 CSRF 令牌添加到响应头
        response["X-CSRFToken"] = request.META.get("CSRF_COOKIE")
        return response

    @action(detail=False, methods=["get"])
    def csrf(self, request):
        csrf_token = get_token(request)
        return Response({"csrfToken": csrf_token})

from .serializers import *
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework import generics, viewsets
from twilio.rest import Client
import random
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


account_sid = "ACae6ed9fce728382f30a13c721e7e2691"
auth_token = "cf61406e85cd696cb4b0867137afab2f"
client = Client(account_sid, auth_token)


class CheckView(viewsets.ModelViewSet):
    queryset = CheckAccaunt.objects.all()
    serializer_class = CheckSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            phone = data['phone']
            key = ''
            for i in range(3):
                key += f"{random.randrange(10)}"
            key += '-'
            for i in range(3):
                key += f"{random.randrange(10)}"
            message = client.messages \
            .create(
                body=f'Your vertification code: {key}',
                from_='+19896013508',
                to=data['phone']
            )
            message.sid
            data = {
                "phone": data['phone'],
                "key": key
            }
            return Response(data)


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        try:
            jwt_object = JWTAuthentication()
            validated_token = jwt_object.get_validated_token(request.headers['token'])
            user = jwt_object.get_user(validated_token)
            user = User.objects.filter(id=user.id).first()
            user_pic = UserInfo.objects.filter(user_id=user.id).first()
            url = ""
            addres = ""
            try:
                if user_pic.profile_pic:
                    url = user_pic.profile_pic.url
                else:
                    url = ""
            except:
                pass

            try:
                addres=user_pic.address
            except:
                pass

            data = {
                "id": user.id,
                "u_id": user_pic.u_id,
                "username": user.username,
                "name": user.first_name,
                "picture": url,
                "address": addres
            }
            return Response(data, status=status.HTTP_200_OK)
        except:
            data = {
                "token": "required"
            }
        return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)

    def update(self, request, *args, **kwargs):
        jwt_object = JWTAuthentication()
        validated_token = jwt_object.get_validated_token(request.headers['token'])
        user = jwt_object.get_user(validated_token)
        userpic = UserInfo.objects.filter(user=user)
        if len(userpic) == 0:
            newuserpic = UserInfo(user_id=user.id)
            newuserpic.save()
        else:
            pass
        userpic = UserInfo.objects.filter(user_id=user.id).first()
        data = request.data
        try:
            if data['first_name']:
                user.first_name = data['first_name']
        except:
            pass

        try:
            if data['picture']:
                userpic.profile_pic = data['picture']
        except:
            pass

        try:
            if data['address']:
                userpic.address = data['address']
        except:
            pass       
        user.save()
        userpic.save()

        return Response({'status':'success'})

class UserInfoView(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class  = UserInfoSerializer


class ResetPasswordView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        jwt_object = JWTAuthentication()
        validated_token = jwt_object.get_validated_token(request.headers['token'])
        user = jwt_object.get_user(validated_token)
        check = user.check_password(request.POST['password'])
        if check == True:
            user.set_password(request.POST['new_password'])
            user.save()
            return Response({'status': 'Success'})
        else:
            return Response({'status': 'Incorrect password'}, status=status.HTTP_406_NOT_ACCEPTABLE)
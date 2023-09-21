from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import GetOrganizationSetializer, InviteSerializer
from .utils import generate_token, EmailManager

# Create your views here.

class OrganizationCreateAPIView(generics.CreateAPIView):
    serializer_class = GetOrganizationSetializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        org = serializer.save()
        data = {
            'id':org.id,
            'name':org.name,
            'email':org.email,
            'lunch_price':org.lunch_price,
            'currency':org.currency,
            'created_at':org.created_at,
            'password':org.password
        }
        res = {
            "message": "Organization created successfully!",
            "code":201,
            "data":data
        }
        return Response(data=res, status=status.HTTP_201_CREATED)


class CreateInviteView(generics.CreateAPIView):
    serializer_class = InviteSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        token = generate_token()
        serializer = self.get_serializer(data=request.data, context={'token':token})
        serializer.is_valid(raise_exception=True)
        invite = serializer.save()

        EmailManager.send_mail(
            subject=f"Free Lunch Invite.",
            recipients=[invite.email],
            template_name="user_invite.html",
            context={"organization":invite.org_id, 'token':invite.token}
        )

        data = {
            'reciepient_email': invite.email,
            'token': invite.token,
            'TTL': invite.TTL
        }
        res = {
            "message": "Invite sent!",
            "code":200,
            "data":data
        }
        return Response(data=res, status=status.HTTP_201_CREATED)




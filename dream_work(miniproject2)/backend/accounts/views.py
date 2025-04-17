from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.http import Http404
from django.core.mail import send_mail
from .models import User, JobSeekerProfile
from .serializers import RegisterSerializer, LoginSerializer, JobSeekerProfileSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            if user.role == 'job_seeker':
                JobSeekerProfile.objects.create(user=user)

            subject = 'Verify Your Email'
            message = f'Click this link to verify: http://localhost:8000/api/auth/verify/{user.verification_uuid}/'
            send_mail(
                subject,
                message,
                'eomino1607@gmail.com',
                [user.email],
                fail_silently=False,
            )
            return Response({"message": "User registered, please verify your email"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(email=serializer.data['email'], password=serializer.data['password'])
            if user and user.is_verified:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'role': user.role
                })
            return Response({"error": "Invalid credentials or email not verified"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    def get(self, request, uuid):
        try:
            user = User.objects.get(verification_uuid=uuid)
            if user.is_verified:
                return Response({"message": "Email already verified"}, status=status.HTTP_200_OK)
            user.is_verified = True
            user.verification_uuid = None
            user.save()
            return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            raise Http404("Verification link is invalid or expired")

class JobSeekerProfileListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles = JobSeekerProfile.objects.filter(user=request.user)
        serializer = JobSeekerProfileSerializer(profiles, many=True)
        return Response(serializer.data)
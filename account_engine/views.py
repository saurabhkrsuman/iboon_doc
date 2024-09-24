from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import CustomUserSerializer, PatientSerializer, PrescriptionSerializer
from .models import Patient, Prescription
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsDoctor
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate


class CustomUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(f"{user.username} user created", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class PatientCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def post(self, request):
        serializer = PatientSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(doctor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def get(self, request):
        patients = Patient.objects.filter(doctor=request.user)
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PatientUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def put(self, request, pk):
        try:
            patient = Patient.objects.get(id=pk, doctor=request.user)  
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PatientSerializer(patient, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrescriptionCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def post(self, request):
        serializer = PrescriptionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(doctor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class PrescriptionListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user == patient.user or request.user == patient.doctor:
            prescriptions = Prescription.objects.filter(patient=patient)
            serializer = PrescriptionSerializer(prescriptions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You do not have permission to view this patient\'s prescriptions'}, status=status.HTTP_403_FORBIDDEN)

    
    
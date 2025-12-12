from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import SolicitudAusencia
from .serializers import SolicitudAusenciaSerializer

def index(request):
    return render(request, 'core/index.html')

class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = SolicitudAusencia.objects.all().order_by('-fecha_solicitud')
    serializer_class = SolicitudAusenciaSerializer

    @action(detail=True, methods=['post'])
    def gestionar(self, request, pk=None):
        solicitud = self.get_object()
        nuevo_estado = request.data.get('estado')
        
        if nuevo_estado not in ['aprobada', 'rechazada']:
            return Response({'error': 'Estado invalido'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(solicitud, data={'estado': nuevo_estado}, partial=True)
        
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({'status': f'Solicitud {nuevo_estado}'})
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
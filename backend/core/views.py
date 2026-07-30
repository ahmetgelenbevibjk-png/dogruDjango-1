from rest_framework import viewsets

class BaseModelViewSet(viewsets.ModelViewSet):
    """
    DELETE isteği geldiğinde veriyi kalıcı olarak silmek yerine
    is_active alanını false yaparak soft-delete uygulayan ortak ViewSet.
    """
    def perform_destroy(self,instance) :
        if hasattr(instance,'soft_delete'):
            instance.soft_delete()
        else:
            instance.is_active=False
            instance.save()
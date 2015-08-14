# Create your views here.
class SoftValidationViewMixin(object):

    @property
    def soft_validation(self):
        # TODO: verifiy, if performance could be improved with
        # @cached_property (as suggested in Two Scoops of Django 1.8)
        return self.object.soft_validation_dict()

""" Views for Django REST Framework - if enabled """

try:
    from rest_framework.decorators import detail_route
    from rest_framework.response import Response

    class SoftValidationAPIViewMixin(object):

        @detail_route(methods=['GET'])
        def validation(self, request, *args, **kwargs):
            self.object = self.get_object()
            data = {
                'view': {
                    'soft_validation': self.object.soft_validation_dict(),
                }
            }
            return Response(data)
        
except ImportError:
    pass



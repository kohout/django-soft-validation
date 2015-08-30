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


class PublishWorkflowViewMixin(object):
    """
    Tries to fetch the publish states
    (formerly known as SoftValidationMixin)

    If the object contains a parent attribute, the view tries to
    fetch the publish-workflow-info from the parent object, else from
    the main object
    """

    def get_context_data(self, *args, **kwargs):
        u = self.request.user
        ctx = super(PublishWorkflowViewMixin, self).get_context_data(
            *args, **kwargs)
        if hasattr(self, 'parent'):
            p = self.parent
        elif hasattr(self, 'object'):
            p = self.object
        else:
            # ListView
            p = None

        if p:
            ctx['can_submit'] = p.oc_can_submit(u)
            ctx['can_publish'] = p.oc_can_publish(u)
            ctx['can_accept'] = p.oc_can_accept(u)
            ctx['can_reject'] = p.oc_can_reject(u)
            ctx['can_delete'] = p.oc_can_delete(u)
            ctx['can_hard_delete'] = p.oc_can_hard_delete(u)
            ctx['can_undelete'] = p.oc_can_undelete(u)
        else:
            # CreateView
            pass

        return ctx

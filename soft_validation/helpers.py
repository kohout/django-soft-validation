# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from .models import SoftValidationResult


def _is_string_and_is_not_empty(string):
    return isinstance(string, basestring) and len(string.strip()) > 0


def _string_empty(obj, field_name):
    field = getattr(obj, field_name)
    verbose_field_name = obj._meta.get_field_by_name(field_name)[0].verbose_name
    result = SoftValidationResult(label=_(u'Please enter a %s' % verbose_field_name))

    if not _is_string_and_is_not_empty(field):
        result.invalid(u'The %s field is empty.' % verbose_field_name, [field_name])

    return result


def field_isset(obj, field_name):
    field = getattr(obj, field_name)
    verbose_field_name = obj._meta.get_field(field_name).verbose_name

    result = SoftValidationResult(
        label=_(u'Please provide a %s' % verbose_field_name))

    if not field:
        result.invalid(u'No %s was set' % verbose_field_name, [field_name])

    return result


def relation_isset(obj, field_name):
    field = getattr(obj, field_name)
    verbose_field_name = obj._meta.get_field(field_name).verbose_name

    result = SoftValidationResult(
        label=_(u'Please provide a %s' % verbose_field_name))

    if not field:
        result.invalid(u'No %s was set' % verbose_field_name, [field_name])

    return result


def related_field_isset(obj, relation_field, field_name):
    relation_check = relation_isset(obj, relation_field)

    if not relation_check.is_valid:
        return relation_check

    rel_obj = getattr(obj, relation_field)

    return field_isset(rel_obj, field_name)

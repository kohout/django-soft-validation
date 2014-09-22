# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
import jsonfield

class SoftValidationResult(object):
    is_valid = True
    error_messages = []
    label = None

    def invalid(self, err_msg, related_fields):
        self.is_valid = False
        self.error_messages.append({
            'msg': unicode(err_msg),
            'related_fields': related_fields
        })

    def __init__(self, *args, **kwargs):
        self.is_valid = kwargs.get('is_valid', True)
        self.error_messages = kwargs.get('error_messages', [])
        self.label = kwargs.get('label', u'(unknown validation)')

    def __dict__(self):
        return {
            'is_valid': self.is_valid,
            'error_messages': self.error_messages,
            'label': unicode(self.label),
        }

class SoftValidationModelMixin(models.Model):

    # a list of SoftValidation-functions
    soft_validators = []

    soft_is_valid = models.BooleanField(
        default=True,
        editable=False,
        verbose_name=_(u'This model is valid'))

    soft_count_valid = models.PositiveIntegerField(
        default=0,
        editable=False,
        help_text=_(u'Number of valid soft validation rules'),
        verbose_name=_(u'Count of valid rules'))

    soft_count_total = models.PositiveIntegerField(
        default=0,
        editable=False,
        help_text=_(u'Number of all soft validation rules'),
        verbose_name=_(u'Count of all rules'))

    soft_completeness = models.FloatField(
        default=1.0,
        editable=False,
        verbose_name=_(u'Grade of completeness (in percent)'))

    soft_validation_result = jsonfield.JSONField(
        editable=False,
        help_text=_(u'Contains detailed information a the soft validation ' \
            u'result as JSON dictionary'),
        verbose_name=_(u'Soft validation result'))

    def soft_validate(self):
        # prepare vars
        count_valid = 0
        is_valid = True
        validation_result = []

        # iterate through registered validators
        for validator in self.soft_validators:
            _result = validator(self)
            if _result.is_valid:
                count_valid += 1
            else:
                is_valid = False
            validation_result.append(_result.__dict__())

        self.soft_is_valid = is_valid
        self.soft_count_valid = count_valid
        self.soft_count_total = len(self.soft_validators)
        self.soft_completeness = (float(count_valid) /
            float(self.soft_count_total))
        self.soft_validation_result = validation_result

    def save(self, *args, **kwargs):
        if kwargs.pop('with_soft_validation', True):
            self.soft_validate()
        super(SoftValidationModelMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True

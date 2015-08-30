# -*- coding: utf-8 -*-

FILTER_STATE_CHOICES = (
    (1, 'New/Changed'),
    (2, 'Submitted'),
    (0, 'Published'),
    (3, 'Rejected'),
    (4, 'Archived'),
)

def get_states(qs, value):
    try:
        value = int(value)
    except ValueError:
        return qs

    qs = qs.filter(is_public=False)
    if value == 0:
        return qs.filter(publish_state=0)
    if value == 1:
        return qs.filter(publish_state=1,
                         editor_state__in=[0, 4])
    if value == 2:
        return qs.filter(publish_state=1,
                         editor_state__in=[1, 2])
    if value == 3:
        return qs.filter(publish_state=1,
                         editor_state=3)
    if value == 4:
        return qs.filter(publish_state=2)

from .event_key import EventKey

def event_factory(event_type, **kwargs):
    event = {EventKey.TYPE: event_type}
    event.update(kwargs)
    return event

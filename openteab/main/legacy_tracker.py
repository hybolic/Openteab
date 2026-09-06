from .mixin.mixin_lifecycle import LifecycleMixin
from .mixin.mixin_config import ConfigMixin
from .mixin.mixin_detection import DetectionMixin
from .mixin.mixin_actions import ActionsMixin
from .mixin.mixin_webhook import WebhookMixin
from .mixin.mixin_remote import RemoteMixin
from .mixin.mixin_recorder import RecorderMixin

class LegacyBiomeTracker(
    LifecycleMixin,
    ConfigMixin,
    DetectionMixin,
    ActionsMixin,
    WebhookMixin,
    RemoteMixin,
    RecorderMixin,
):
    pass

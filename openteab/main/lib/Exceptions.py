class DuplicateRegistryError(ValueError):
    """Raised when trying to register a duplicate name."""
    pass

class RegistryMissingError(ValueError):
    """Raised when trying to retrieve a registry but its missing."""
    pass


#properties
class classproperty:
    def __init__(self, func):
        self.func = func
    def __get__(self, instance, owner):
        return self.func()
    
GetTypeName = lambda cls: getattr(cls, "__name__", type(cls).__name__)
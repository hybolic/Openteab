class DuplicateRegistryError(ValueError):
    """Raised when trying to register a duplicate name."""
    pass

class RegistryMissingError(ValueError):
    """Raised when trying to retrieve a registry but its missing."""
    pass
    
GetTypeName = lambda cls: getattr(cls, "__name__", type(cls).__name__)
from dataclasses import dataclass


@dataclass(frozen=True)
class BaseDTO:
    @classmethod
    def from_orm[T](cls: type[T], obj: object) -> T:
        missing_fields = [k for k in cls.__annotations__.keys() if not hasattr(obj, k)]
        if missing_fields:
            raise AttributeError(
                f"Object '{obj.__class__.__name__}' does not have attributes {missing_fields}"
            )

        d = {k: getattr(obj, k) for k in cls.__annotations__.keys()}

        return cls(**d)

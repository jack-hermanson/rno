from wtforms import StringField
from wtforms.fields.simple import PasswordField

# noinspection PyTypeChecker
original_init = StringField.__init__


# Hacky thing to automatically strip inputs
# def new_init(self: StringField, *args: tuple[Any, ...], **kwargs: dict[str, Any] | list) -> None:
def new_init(self: StringField, *args, **kwargs) -> None:
    if self.__class__ is not PasswordField:
        filters = kwargs.pop("filters", [])
        filters = [lambda x: x.strip() if x else x, *filters]
        kwargs["filters"] = filters
        original_init(self, *args, **kwargs)
    else:
        original_init(self, *args, **kwargs)


StringField.__init__ = new_init

# lowrapper - Client

from typing import (
    overload, Protocol, TypeVar, Generic, Callable, Type, NoReturn,
    Literal, Union, Any
)

from requests import Response, request
from inspect import isfunction


Method = Union[Literal[
    "GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"
], str]


NoRequestT = TypeVar("NoRequestT", bound=Callable[..., Any])
def norequest(func: NoRequestT) -> NoRequestT:
    "This is a decorator to indicate that the function is not prepared to make a request."
    func.__lowrapper_norequest__ = True # type: ignore
    return func


def _trial_error(e: TypeError, name: str) -> NoReturn:
    if any(word in str(e) for word in ("takes", "but", "__init__()")):
        raise TypeError(str(e).replace("__init__", name))
    else:
        raise e


PathT = TypeVar("PathT", bound="_PathGenerator")
class _PathGenerator(Generic[PathT]):
    def __init__(self, path: str):
        self.path = path

    def _get_class(self, name: str) -> Type[PathT]:
        if name in getattr(self, "__annotations__", {}):
            return self.__annotations__[name]
        return type(
            "PathSub", (globals()["Path"],), {
                name: getattr(self.__class__, name)
                for name in dir(self.__class__)
                if name.startswith("__lowrapper_")
            }
        )

    def __getitem__(self, name: str) -> PathT:
        return self.__getattr__(name)

    def __getattr__(self, name: str) -> PathT:
        self.path += f"{name}/"
        return self._get_class(name)(self.path)


class PathGenerator(_PathGenerator["PathGenerator"]):
    ...


ResponseT = TypeVar("ResponseT")
ClientT = TypeVar("ClientT", bound="Client")
class Path(_PathGenerator["Path[ResponseT]"], Generic[ResponseT]):
    def __init__(self, path: str, client: ClientT):
        self.path, self.client = path, client
        self.__request__ = self.client.__request__
        self._locked = False

    def __init_subclass__(cls):
        super().__init_subclass__()
        for name in dir(cls):
            if (not name.startswith("_") and isfunction(obj := getattr(cls, name))
                    and not hasattr(obj, "__lowrapper_norequest__")):
                setattr(cls, f"__lowrapper_{name}__", obj)
                delattr(cls, name)

    class _Request(Protocol):
        def __call__(self, method: Method, **kwargs) -> ResponseT:
            ...

    __call__: Union[_Request, Callable[..., Union[ResponseT, Any]]]
    def __call__(self, *args, **kwargs): # type: ignore
        self._locked = True
        try:
            if hasattr(
                self, name:="".join((
                    "__lowrapper_",
                    self.path[:-1][self.path[:-1].rfind("/")+1:],
                    "__"
                ))
            ):
                return getattr(self, name)(*args, **kwargs)
            return self.__request__(self, *args, **kwargs)
        except Exception as e:
            if isinstance(e, TypeError):
                _trial_error(e, name)
            else:
                self._locked = False
                raise e
        finally:
            self._locked = False

    def __getitem__(self, name: str) -> "Path[ResponseT]":
        return super().__getitem__(name)

    def __getattr__(self, name: str) -> "Path[ResponseT]":
        if self._locked:
            raise AttributeError(f"{self.__class__.__name__} has no attribute {name}.")
        else:
            self.path += f"{name}/"
            try:
                return self._get_class(name)(self.path, self.client)
            except TypeError as e:
                _trial_error(e, name)


class _BaseRequest(Protocol):
    def __call__(
        self, path: Any, method: Method, **kwargs
    ) -> Any:
        ...


class Client(Path):
    def __init__(self, path: str = ""):
        self.__default_path = path
        super().__init__(path, self)

    class _Request(_BaseRequest):
        def __call__(
            self, path: Path[ResponseT], method: Method, **kwargs
        ) -> ResponseT:
            ...

    __request__: Union[_Request, _BaseRequest]
    def __request__(self, path, method, **kwargs): # type: ignore
        return request(method, path.path, **kwargs)

    def __getattr__(self, name: str) -> Path[ResponseT]:
        self.path = self.__default_path
        return super().__getattr__(name)
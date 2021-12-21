"""Attributes
----------
Method : Union[Literal["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"], str]
    Type for request method.
Response
    `requests.Response`
request
    `requests.request`"""
# lowrapper - Client

from typing import TypeVar, Generic, Callable, Type, NoReturn, Literal, Union, Any

from requests import Response, request
from inspect import isfunction


Method = Union[Literal[
    "GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"
], str]


NoRequestT = TypeVar("NoRequestT", bound=Callable[..., Any])
def norequest(func: NoRequestT) -> NoRequestT:
    """This is a decorator to indicate that the function is not prepared to make a request.

    Examples
    --------
    ```python
    class MyClient(Client):

        # Mark prepare_data as not a request function.
        @norequest
        def prepare_data(self, message: Message) -> dict:
            \"\"\"Prepare request base data.  
            This function is not a request function.\"\"\"
            ...

        def send(self, message: Message) -> Response:
            "Send message"
            data = self.preapre_data(message)
            return self.__request__(self, method="POST", data=data)
    ```"""
    func.__lowrapper_norequest__ = True # type: ignore
    return func


def _trial_error(e: TypeError, name: str) -> NoReturn:
    if any(word in str(e) for word in ("takes", "but", "__init__()")):
        raise TypeError(str(e).replace("__init__", name))
    else:
        raise e


def _raise_ate(self, name: str) -> NoReturn:
    raise AttributeError(f"{self.__class__.__name__} has no attribute {name}.")


PathT = TypeVar("PathT", bound="_PathGenerator")
class _PathGenerator(Generic[PathT]):

    __cls_name__ = "_PathGenerator"

    def __init__(self, path: str):
        self.path = path

    def _get_class(self, name: str) -> Type[PathT]:
        if name in getattr(self, "__annotations__", {}):
            return self.__annotations__[name]
        return type(
            "PathSub", (globals()[self.__cls_name__],), {
                name: getattr(self.__class__, name)
                for name in dir(self.__class__)
                if name.startswith("__lowrapper_")
            }
        )

    def __getitem__(self, name: str) -> PathT:
        return self.__getattr__(name)

    def __getattr__(self, name: str) -> PathT:
        if name.startswith("_"):
            _raise_ate(self, name)
        else:
            self.path += f"{name}/"
            return self._get_class(name)(self.path)


class PathGenerator(_PathGenerator["PathGenerator"]):
    """Class for creating the API endpoint path.
    When a nonexistent attribute is accessed, the name of the accessed attribute is added to the endpoint path.  
    And returns this class.  
    This class allows you to create an endpoint path without using a string.

    Parameters
    ----------
    path : str
        Default path.

    Attributes
    ----------
    path : str
        Configured path.

    Examples
    --------
    ```python
    from lowrapper import PathGenerator

    path = PathGenerator("https://some.web.site/")
    print(path.api.test.endpoint.path)
    # https://some.web.site/api/test/endpoint/
    ```

    Notes
    -----
    If you want to create attributes that you don't want to include in the path, place an underscore at the beginning of the name."""
    __cls_name__ = "PathGenerator"


ResponseT = TypeVar("ResponseT")
ClientT = TypeVar("ClientT", bound="Client")
class Path(_PathGenerator["Path[ResponseT]"], Generic[ResponseT]):
    """Class returned when accessing some attribute of the `Client` or `Path` class.  
    It inherits from `PathGenerator` and uses this class to construct the endpoint URL.  
    It also returns an instance of the class specified in the annotation if the annotation is in a class with the name of the attribute accessed.  
    The class to be specified for this annotation is the class that inherits from `Path` or `Path`.
    
    Parameters
    ----------
    path : str
        First path.
    client : Client
        The client to push API.

    Attributes
    ----------
    path : str
        Configured endpoint path.
    client : Client

    Notes
    -----
    If you want to make endpoint path, you should use `PathGenerator`.  
    If you want to create attributes that you don't want to include in the path, place an underscore at the beginning of the name."""

    __cls_name__ = "Path"

    def __init__(self, path: str, client: ClientT):
        self.path, self.client = path, client
        self.__request__ = self.client.__request__
        self.__locked = False

    def __init_subclass__(cls):
        super().__init_subclass__()
        for name in dir(cls):
            if (not name.startswith("_") and isfunction(obj := getattr(cls, name))
                    and not hasattr(obj, "__lowrapper_norequest__")):
                setattr(cls, f"__lowrapper_{name}__", obj)
                delattr(cls, name)

    def __call__(self, *args, **kwargs) -> ResponseT:
        """Call `__request__`.  
        If the last attribute accessed is callable by a function, the function is called."""
        self.__locked = True
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
                self.__locked = False
                raise e
        finally:
            self.__locked = False

    def __getitem__(self, name: str) -> "Path[ResponseT]":
        return super().__getitem__(name)

    def __getattr__(self, name: str) -> "Path[ResponseT]":
        if self.__locked or name.startswith("_"):
            _raise_ate(self, name)
        else:
            self.path += f"{name}/"
            try:
                return self._get_class(name)(self.path, self.client)
            except TypeError as e:
                _trial_error(e, name)


ClientResponseT = TypeVar("ClientResponseT", bound=Union[Response, Any])
class Client(Path[ClientResponseT], Generic[ClientResponseT]):
    """This is a client class for tapping the API, which extends the `Path` class.  
    So it works like `Path`.  
    Also, if you are using mypy, you need to specify the return value when hitting the API as follows:
    ```python
    from lowrapper import Client, Response

    client: Client[Response] = Client(BASE_URL)
    # or
    client = Client[Response](BASE_URL)
    ```
    (`# type: ignore` to ignore.)  
    This is to ensure that type completion works well when you override a request function and have the return value automatically made into a dictionary, or when you use another library for the request.  
    It also allows type completion of the return value when hitting the API.  
    When you access an attribute of this class as follows, the name of the attribute is automatically appended to the path of the requesting endpoint.  
    You can then make a request by calling that attribute.  
    The attribute can be undefined.  
    attribute returns `Path`.

    Parameters
    ----------
    path : str
        Default path. (Base url)

    ## `__request__` method
    This function is called when making a request.  
    By default, the `requests` library is used to make requests with the passed keyword arguments along with the path in the passed `Path` class.  
    You make a request when you call an instance of `Path`.  
    You can override this function to make the return value different.  
    For example, if all the data in the API response is JSON, adding `.json () `to each request can be tedious, so you can override this function and return JSON as a dictionary.  
    If you are using the asynchronous `Client` class, `aiohttp` will be used in the request.

    Parameters
    ----------
    self : Client
    path : Union[Path, Client]
        `Path` class used to create the requested path.  
        Get the requested path from this class from the `path` attribute.  
        If the access is from an attribute of the `Client` class, the `Client` class is passed instead of the `Path` class.  
        But you don't have to worry about it.

    Notes
    -----
    For the asynchronous version of `Client`, this function returns a coroutine by default."""

    __cls_name__ = "Path"

    def __init__(self, path: str):
        self.__default_path = path
        super().__init__(path, self)

    def __request__(self, path: Union[Path[ClientResponseT], Any], **kwargs) -> Union[ClientResponseT, Any]:
        if "url" not in kwargs:
            kwargs["url"] = path.path
        return request(**kwargs) # type: ignore

    def __getattr__(self, name: str) -> Path[ClientResponseT]:
        if name.startswith("_"):
            _raise_ate(self, name)
        else:
            self.path = self.__default_path
            return Path.__getattr__(self, name) # type: ignore
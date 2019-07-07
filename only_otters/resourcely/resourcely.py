# std
import json
import os
import pathlib
import re
from argparse import Namespace
from dataclasses import dataclass
from typing import Union, Any

# other
import yaml


__folder__ = pathlib.Path(__file__).parent


def ensure_field(dictlike: dict, fieldname: str) -> Any:
    """Ensure the required field is found in the data structure."""
    sentinel = object()
    value = dictlike.get(fieldname, sentinel)

    if value is sentinel:
        raise UserWarning('{!r} is a required field'.format(fieldname))

    return value


@dataclass
class Resource:
    """
    A wrapper around a resource file to make it accessible through the Python
    import mechanism. Allow to exile resource paths from the code to static
    config files.
    """

    name: str
    url: Union[str, 'os.PathLike[Any]', pathlib.Path]
    md5hash: str = None

    @property
    def str(self) -> str:
        return str(self.url)

    @property
    def QUrl(self) -> 'QUrl':
        """Return a QUrl object built from the original url."""
        from PyQt5.QtCore import QUrl
        return QUrl.fromLocalFile(os.fspath(self))

    def __fspath__(self):
        return os.fspath(self.absolute)

    @property
    def absolute(self) -> pathlib.Path:
        """Return the absolute path of the stored Path object."""
        return pathlib.Path(self.url).absolute()


def _parse_list(resources: list, prefix=pathlib.Path()) -> Namespace:
    namespace = Namespace()

    for resource in resources:
        if type(resource) == str:
            resource = {
                'name': resource,
                'url': resource
            }
        print(resource)

        url = ensure_field(resource, 'url')
        name = resource.get('name')
        if name is None:
            name = url

        namespace.name = Resource(
            name=name,
            url=prefix / url
        )

    return namespace


def _parse_dict(resources: dict, prefix=pathlib.Path()) -> Namespace:
    """
    Parse a dict structure found in a resources configuration file.
    The special (type=namespace) key allows you to nest namespaces, otherwise
    the content will be processed as a list of [name -> url] pairs.
    """
    if resources.get('type') == 'namespace':
        del resources['type']
        return Namespace(**{
            key: parse(value, prefix=prefix)
            for key, value in resources.items()
        })

    return Namespace(**{
        key: Resource(
            name=key,
            url=prefix / value
        )
        for key, value in resources.items()
    })


def load(filepath) -> dict:
    """Load the resource config file and automatically detects the required loader depending
    on the file extension."""
    strpath = os.fspath(filepath)

    if not strpath:
        raise UserWarning("Resouce loader: 'filepath' is empty.")

    if '.' not in strpath:
        raise UserWarning('Resouce loader: path has no file extension.')

    extension = strpath.split('.')[-1]

    sentinel = object()
    loader = _EXT_LOADERS.get(extension, sentinel)
    if loader is sentinel:
        raise UserWarning('Resouce loader: No loader for {!r} files.'.format(extension))

    return loader(open(filepath))


def parse(resources: Union[dict, list], prefix=pathlib.Path()) -> Namespace:
    """
    Parse a resource config file. Detect the parsing method depending on the resource to parse.
    Resources can only be parsed from [list, dict] elements.
    """
    sentinel = object()
    parser = _TYPE_PARSERS.get(type(resources), sentinel)
    if parser is sentinel:
        raise UserWarning(
            "Invalid 'resource' type: %s."
            "Must be one of those: %s" % (
                type(resources).__qualname__,
                ', '.join(type_.__qualname__ for type_ in _TYPE_PARSERS.keys())
            )
        )
    return parser(resources, prefix=prefix)


_TYPE_PARSERS = {
    list: _parse_list,
    dict: _parse_dict
}

_EXT_LOADERS = {
    'json': json.load,
    'yml': yaml.safe_load,
    'yaml': yaml.safe_load
}


def from_located_file(filepath='resources.yml', location=None, near=None) -> Namespace:
    """Load a resource namespace from a file located in the 'location' folder, or in the parent
    folder of the path provided in 'near'."""

    if (
        near is None and location is None or
        near and location
    ):
        raise UserWarning(
            "'location' and 'near' can't both be None or both be provided. Choose one.")

    folder = pathlib.Path()

    if location:
        folder = pathlib.Path(location)

    if near:
        folder = pathlib.Path(near).parent

    data = yaml.safe_load(open(folder / filepath))
    resources = ensure_field(data, 'resources')
    return parse(resources, prefix=folder)


def expand(resources: Namespace, context: dict):
    """Expand the namespace in another directory. This function was designed to
    allow the user to expand the resource namespace in a module's namespace."""
    for key, value in dict(resources._get_kwargs()).items():
        context[key] = value


def get_domain_name(url) -> str:
    """Retrieve domain name without protocol prefix or subpath."""
    return re.search(r'https?://([\w.-]+?)(?:/.*)?$', url).groups()[0]


__all__ = [
    'get_domain_name',
    'expand',
    'Resource',
    'load',
    'parse',
    'from_located_file',
    'ensure_field'
]

"""
ubw debug module

"""

from abc import abstractmethod
from cement.core.interface import Interface
from cement.core.handler import Handler
from cement.utils.misc import is_true, minimal_logger

LOG = minimal_logger(__name__)


class DebugInterface(Interface):

    """
    This class defines the Debug Interface.  Handlers that implement this
    interface must provide the methods and attributes defined below. In
    general, most implementations should sub-class from the provided
    :class:`BuildHandler` base class as a starting point.
    """
    class Meta:

        """Handler meta-data."""

        #: The string identifier of the interface.
        interface = 'debug'

    @abstractmethod
    def debug(self, *args, **kw):
        pass


class DebugHandler(DebugInterface, Handler):

    """
    Debug handler implementation.

    """

    pass  # pragma: nocover


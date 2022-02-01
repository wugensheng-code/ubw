"""
ubw flash module

"""

from abc import abstractmethod
from cement.core.interface import Interface
from cement.core.handler import Handler
from cement.utils.misc import is_true, minimal_logger

LOG = minimal_logger(__name__)


class FlashInterface(Interface):

    """
    This class defines the Flash Interface.  Handlers that implement this
    interface must provide the methods and attributes defined below. In
    general, most implementations should sub-class from the provided
    :class:`FlashHandler` base class as a starting point.
    """
    class Meta:

        """Handler meta-data."""

        #: The string identifier of the interface.
        interface = 'flash'

    @abstractmethod
    def flash(self, *args, **kw):
        pass


class FlashHandler(FlashInterface, Handler):

    """
    Flash handler implementation.

    """

    pass  # pragma: nocover


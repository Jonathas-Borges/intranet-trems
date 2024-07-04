"""Init and utils."""
from zope.i18nmessageid import MessageFactory

import logging


PACKAGE_NAME = "intranet_trems"

_ = MessageFactory("intranet_trems")

logger = logging.getLogger("intranet_trems")

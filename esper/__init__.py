from .world import World, CachedWorld, ParallelWorld
from .templates import Processor, ParallelProcessor

from .meta import (author as __author__,
                   version as __version__,
                   license as __license__)

__copyright__ = __author__

__all__ = ("Processor", "ParallelProcessor", "World", "CachedWorld", "ParallelWorld")

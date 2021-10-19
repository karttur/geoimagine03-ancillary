"""
ancillary
==========================================

Package belonging to Karttur´s GeoImagine Framework.

Author
------
Thomas Gumbricht (thomas.gumbricht@karttur.com)

"""

from .version import __version__, VERSION, metadataD

from .ancillary import ProcessAncillary

from .searchjson import SearchJsonTandemX, UnZipJsonTandemX

__all__ = ['ProcessAncillary']
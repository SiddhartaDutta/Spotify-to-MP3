"""
Dataclass dedicated to creating a structure for metadata.
"""

from dataclasses import dataclass

@dataclass
class metaDataFrame:
    albumName: str = ''
    releaseDate: str = ''
    genre: str = ''
    title: str = ''
    trackNumber: str = ''
    albumArtist: str = ''
    songArtist: str = ''

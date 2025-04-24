from pydantic import BaseModel

class DataFrameRow(BaseModel):
    track_name: str
    track_artist: str
    track_popularity: int
    track_album_name: str
    playlist_genre: str
    playlist_subgenre: str
    loudness: float
    duration_in_minutes: float

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.track_album_release_date = str(kwargs['track_album_release_date'])

class DataFrameJson(BaseModel):
    df: list[dict]
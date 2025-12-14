from app.dal.music_dal import MusicDAL
from app.models.music import Music
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.utils.logger import logger

class GlobalMusicContext:
    _instance = None
    _music_list_cache: List[Music] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GlobalMusicContext, cls).__new__(cls)
        return cls._instance

    async def initialize(self, session: AsyncSession):
        if self._music_list_cache is None:
            logger.info("GlobalMusicContext: Ładowanie pełnej listy utworów z bazy danych...")
            musicDAL = MusicDAL(session)
            
            self._music_list_cache = await musicDAL.get_music_columns(
                filter_not_none=[
                    Music.spotify_features,
                    Music.embedding_emotions,
                    Music.embedding_tags,
                    Music.embedding
                ]
            )
            logger.info(f"GlobalMusicContext: Załadowano {len(self._music_list_cache)} utworów do cache'u.")
        
    def get_full_music_list(self) -> List[Music]:
        """Zwraca listę z pamięci. Zawsze używać po initialize()."""
        if self._music_list_cache is None:
            raise RuntimeError("GlobalMusicContext nie został zainicjowany. Uruchom .initialize() przed użyciem.")
        return self._music_list_cache
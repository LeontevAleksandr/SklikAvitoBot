"""
Менеджер сессий для сохранения cookies и состояния
"""
import json
from pathlib import Path
from datetime import datetime, timedelta
from utils.logger import setup_logger

logger = setup_logger(__name__)


class SessionManager:
    """Управление сессиями браузера"""
    
    def __init__(self, session_dir: Path = None):
        """
        Инициализация менеджера сессий
        
        Args:
            session_dir: Директория для хранения сессий
        """
        self.session_dir = session_dir or Path(__file__).parent.parent / "sessions"
        self.session_dir.mkdir(exist_ok=True)
        self.session_file = self.session_dir / "avito_session.json"
    
    def save_session(self, context, session_name: str = "default") -> None:
        """
        Сохраняет текущую сессию браузера
        
        Args:
            context: Контекст браузера Playwright
            session_name: Имя сессии
        """
        try:
            session_data = {
                'name': session_name,
                'timestamp': datetime.now().isoformat(),
                'expires': (datetime.now() + timedelta(days=7)).isoformat(),
            }
            
            # Сохраняем состояние контекста
            storage_state = context.storage_state()
            session_data['storage_state'] = storage_state
            
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Сессия '{session_name}' успешно сохранена")
            
        except Exception as e:
            logger.error(f"Ошибка при сохранении сессии: {e}")
    
    def load_session(self, session_name: str = "default") -> dict:
        """
        Загружает сохраненную сессию
        
        Args:
            session_name: Имя сессии
            
        Returns:
            Данные сессии или None если сессия не найдена/устарела
        """
        try:
            if not self.session_file.exists():
                logger.info("Сохраненная сессия не найдена, создается новая")
                return None
            
            with open(self.session_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            # Проверяем срок действия
            expires = datetime.fromisoformat(session_data['expires'])
            if datetime.now() > expires:
                logger.warning("Сессия устарела, будет создана новая")
                self.session_file.unlink()
                return None
            
            logger.info(f"Загружена сессия '{session_name}' от {session_data['timestamp']}")
            return session_data.get('storage_state')
            
        except Exception as e:
            logger.error(f"Ошибка при загрузке сессии: {e}")
            return None
    
    def clear_session(self, session_name: str = "default") -> None:
        """
        Удаляет сохраненную сессию
        
        Args:
            session_name: Имя сессии
        """
        try:
            if self.session_file.exists():
                self.session_file.unlink()
                logger.info(f"Сессия '{session_name}' удалена")
        except Exception as e:
            logger.error(f"Ошибка при удалении сессии: {e}")
    
    def is_session_valid(self) -> bool:
        """
        Проверяет валидность текущей сессии
        
        Returns:
            True если сессия существует и не устарела
        """
        if not self.session_file.exists():
            return False
        
        try:
            with open(self.session_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            expires = datetime.fromisoformat(session_data['expires'])
            return datetime.now() <= expires
            
        except Exception:
            return False
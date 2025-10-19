"""
Парсер входной строки пользователя для системы рекомендаций игр
Извлекает возраст и предпочтения из текстового ввода
"""

import re
from typing import Dict, List, Optional

class InputParser:
    def __init__(self):
        # Паттерны для извлечения возраста
        self.age_patterns = [
            r'мне\s+(\d+)\s+лет',
            r'возраст\s*:?\s*(\d+)',
            r'(\d+)\s+лет',
            r'я\s+(\d+)\s+лет'
        ]
        
        # Список известных жанров для поиска
        self.known_genres = [
            'RPG', 'Action', 'Adventure', 'Strategy', 'Simulation', 
            'Puzzle', 'Indie', 'Horror', 'Racing', 'Sports'
        ]
        
        # Паттерны для поиска жанров
        self.genre_patterns = [
            r'мне\s+нравятся?\s*:?\s*([^.]+)',
            r'люблю\s*:?\s*([^.]+)',
            r'интересы?\s*:?\s*([^.]+)',
            r'предпочтения?\s*:?\s*([^.]+)',
            r'жанры?\s*:?\s*([^.]+)'
        ]
    
    def parse_input(self, user_input: str) -> Dict[str, any]:
        """
        Парсит входную строку пользователя и извлекает возраст и предпочтения
        
        Args:
            user_input: Строка ввода пользователя
            
        Returns:
            Словарь с извлеченными данными: {'age': int, 'genres': list}
        """
        user_input = user_input.strip()
        
        # Извлекаем возраст
        age = self._extract_age(user_input)
        
        # Извлекаем жанры
        genres = self._extract_genres(user_input)
        
        return {
            'age': age,
            'genres': genres,
            'original_input': user_input
        }
    
    def _extract_age(self, text: str) -> Optional[int]:
        """
        Извлекает возраст из текста
        
        Args:
            text: Текст для анализа
            
        Returns:
            Возраст или None если не найден
        """
        text_lower = text.lower()
        
        for pattern in self.age_patterns:
            match = re.search(pattern, text_lower)
            if match:
                try:
                    age = int(match.group(1))
                    if 3 <= age <= 100:  # Разумные ограничения возраста
                        return age
                except ValueError:
                    continue
        
        return None
    
    def _extract_genres(self, text: str) -> List[str]:
        """
        Извлекает жанры из текста
        
        Args:
            text: Текст для анализа
            
        Returns:
            Список найденных жанров
        """
        text_lower = text.lower()
        found_genres = []
        
        # Сначала ищем по паттернам
        for pattern in self.genre_patterns:
            match = re.search(pattern, text_lower)
            if match:
                genres_text = match.group(1)
                found_genres.extend(self._parse_genres_from_text(genres_text))
        
        # Если не нашли по паттернам, ищем прямые упоминания жанров
        if not found_genres:
            for genre in self.known_genres:
                if genre.lower() in text_lower:
                    found_genres.append(genre)
        
        # Убираем дубликаты и возвращаем
        return list(set(found_genres))
    
    def _parse_genres_from_text(self, genres_text: str) -> List[str]:
        """
        Парсит жанры из текста, разделенного запятыми или другими разделителями
        
        Args:
            genres_text: Текст с жанрами
            
        Returns:
            Список найденных жанров
        """
        found_genres = []
        
        # Специальные маппинги для русских названий
        genre_mappings = {
            'инди': 'Indie',
            'инди-игры': 'Indie',
            'инди игры': 'Indie',
            'ролевые': 'RPG',
            'ролевые игры': 'RPG',
            'экшен': 'Action',
            'экшн': 'Action',
            'приключения': 'Adventure',
            'стратегия': 'Strategy',
            'стратегии': 'Strategy',
            'симулятор': 'Simulation',
            'симуляторы': 'Simulation',
            'головоломки': 'Puzzle',
            'головоломка': 'Puzzle',
            'ужасы': 'Horror',
            'хоррор': 'Horror',
            'гонки': 'Racing',
            'спорт': 'Sports',
            'спортивные': 'Sports'
        }
        
        # Сначала проверяем специальные маппинги
        text_lower = genres_text.lower()
        for russian_name, english_name in genre_mappings.items():
            if russian_name in text_lower:
                found_genres.append(english_name)
        
        # Разделяем по запятым, точкам, и другим разделителям
        parts = re.split(r'[,.\-;]', genres_text)
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
                
            # Ищем точные совпадения с известными жанрами
            for genre in self.known_genres:
                if genre.lower() in part.lower():
                    found_genres.append(genre)
        
        return found_genres
    
    def validate_input(self, parsed_data: Dict[str, any]) -> Dict[str, any]:
        """
        Валидирует и дополняет распарсенные данные
        
        Args:
            parsed_data: Данные после парсинга
            
        Returns:
            Валидированные данные с дополнительной информацией
        """
        result = parsed_data.copy()
        
        # Проверяем возраст
        if result['age'] is None:
            result['age_valid'] = False
            result['age_error'] = "Возраст не найден в тексте"
        else:
            result['age_valid'] = True
            result['age_error'] = None
        
        # Проверяем жанры
        if not result['genres']:
            result['genres_valid'] = False
            result['genres_error'] = "Жанры не найдены в тексте"
        else:
            result['genres_valid'] = True
            result['genres_error'] = None
        
        # Общая валидность
        result['is_valid'] = result['age_valid'] and result['genres_valid']
        
        return result
    
    def get_parsing_examples(self) -> List[str]:
        """
        Возвращает примеры правильного ввода для пользователя
        
        Returns:
            Список примеров
        """
        return [
            "Мне 13 лет, мне нравятся: RPG, инди-игры",
            "Возраст: 25, люблю Action и Strategy",
            "Я 18 лет, интересы: Horror, Adventure",
            "Мне 30 лет, предпочтения: Simulation, Puzzle",
            "Возраст 16, нравятся Racing и Sports"
        ]

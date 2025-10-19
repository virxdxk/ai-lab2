"""
Движок рекомендаций игр на основе базы знаний
Использует логические запросы для поиска подходящих игр
"""

from typing import List, Dict, Set, Tuple
from game_knowledge_base import GameKnowledgeBase

class RecommendationEngine:
    def __init__(self, knowledge_base: GameKnowledgeBase):
        self.kb = knowledge_base
    
    def get_recommendations(self, age: int, preferred_genres: List[str]) -> Dict[str, any]:
        """
        Получает рекомендации игр на основе возраста и предпочтений
        
        Args:
            age: Возраст пользователя
            preferred_genres: Список предпочитаемых жанров
            
        Returns:
            Словарь с рекомендациями и обоснованием
        """
        # Логические запросы к базе знаний
        age_appropriate_games = self._query_age_appropriate_games(age)
        genre_games = self._query_genre_games(preferred_genres)
        
        # Находим пересечение (игры подходящие и по возрасту, и по жанру)
        recommended_games = self._intersect_games(age_appropriate_games, genre_games)
        
        # Если пересечение пустое, расширяем поиск
        if not recommended_games:
            recommended_games = self._expand_recommendations(age, preferred_genres)
        
        # Сортируем по релевантности
        sorted_recommendations = self._rank_recommendations(recommended_games, age, preferred_genres)
        
        return {
            'recommendations': sorted_recommendations,
            'reasoning': self._generate_reasoning(age, preferred_genres, sorted_recommendations),
            'total_found': len(sorted_recommendations),
            'age_appropriate_count': len(age_appropriate_games),
            'genre_matching_count': len(genre_games)
        }
    
    def _query_age_appropriate_games(self, age: int) -> Set[str]:
        """
        Логический запрос: найти все игры подходящие по возрасту
        
        Args:
            age: Возраст пользователя
            
        Returns:
            Множество игр подходящих по возрасту
        """
        appropriate_games = set()
        
        for game, min_age in self.kb.age_ratings.items():
            if min_age <= age:
                appropriate_games.add(game)
        
        return appropriate_games
    
    def _query_genre_games(self, genres: List[str]) -> Set[str]:
        """
        Логический запрос: найти все игры указанных жанров
        
        Args:
            genres: Список жанров
            
        Returns:
            Множество игр указанных жанров
        """
        genre_games = set()
        
        for genre in genres:
            games = self.kb.get_games_by_genre(genre)
            genre_games.update(games)
        
        return genre_games
    
    def _intersect_games(self, games1: Set[str], games2: Set[str]) -> Set[str]:
        """
        Логическая операция пересечения множеств игр
        
        Args:
            games1: Первое множество игр
            games2: Второе множество игр
            
        Returns:
            Пересечение множеств
        """
        return games1.intersection(games2)
    
    def _expand_recommendations(self, age: int, preferred_genres: List[str]) -> Set[str]:
        """
        Расширяет поиск рекомендаций если точного совпадения нет
        
        Args:
            age: Возраст пользователя
            preferred_genres: Предпочитаемые жанры
            
        Returns:
            Расширенный набор рекомендаций
        """
        expanded_games = set()
        
        # Стратегия 1: Игры подходящие по возрасту из популярных
        age_appropriate = self._query_age_appropriate_games(age)
        popular_games = set(self.kb.get_games_by_popularity('very_popular'))
        expanded_games.update(age_appropriate.intersection(popular_games))
        
        # Стратегия 2: Легкие игры подходящие по возрасту
        easy_games = set(self.kb.get_games_by_difficulty('easy'))
        expanded_games.update(age_appropriate.intersection(easy_games))
        
        # Стратегия 3: Если пользователь молодой, добавляем семейные игры
        if age < 16:
            family_friendly_genres = ['Puzzle', 'Racing', 'Sports']
            family_games = self._query_genre_games(family_friendly_genres)
            expanded_games.update(age_appropriate.intersection(family_games))
        
        return expanded_games
    
    def _rank_recommendations(self, games: Set[str], age: int, preferred_genres: List[str]) -> List[Dict[str, any]]:
        """
        Ранжирует рекомендации по релевантности
        
        Args:
            games: Множество игр для ранжирования
            age: Возраст пользователя
            preferred_genres: Предпочитаемые жанры
            
        Returns:
            Отсортированный список рекомендаций с метаданными
        """
        ranked_games = []
        
        for game in games:
            score = self._calculate_relevance_score(game, age, preferred_genres)
            game_info = {
                'name': game,
                'genre': self.kb.get_game_genre(game),
                'age_rating': self.kb.get_game_age_rating(game),
                'relevance_score': score,
                'platforms': self._get_game_platforms(game)
            }
            ranked_games.append(game_info)
        
        # Сортируем по релевантности (убывание)
        ranked_games.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return ranked_games
    
    def _calculate_relevance_score(self, game: str, age: int, preferred_genres: List[str]) -> float:
        """
        Вычисляет релевантность игры для пользователя
        
        Args:
            game: Название игры
            age: Возраст пользователя
            preferred_genres: Предпочитаемые жанры
            
        Returns:
            Оценка релевантности (0.0 - 1.0)
        """
        score = 0.0
        
        # Базовый балл за соответствие возрасту
        game_age = self.kb.get_game_age_rating(game)
        if game_age <= age:
            score += 0.3
        
        # Бонус за соответствие жанру
        game_genre = self.kb.get_game_genre(game)
        if game_genre in preferred_genres:
            score += 0.4
        
        # Бонус за популярность
        if game in self.kb.get_games_by_popularity('very_popular'):
            score += 0.2
        elif game in self.kb.get_games_by_popularity('popular'):
            score += 0.1
        
        # Бонус за подходящую сложность для возраста
        if age < 16 and game in self.kb.get_games_by_difficulty('easy'):
            score += 0.1
        elif age >= 16 and game in self.kb.get_games_by_difficulty('medium'):
            score += 0.1
        
        return min(score, 1.0)  # Ограничиваем максимальным значением
    
    def _get_game_platforms(self, game: str) -> List[str]:
        """
        Получает платформы для игры
        
        Args:
            game: Название игры
            
        Returns:
            Список платформ
        """
        platforms = []
        for platform, games in self.kb.platforms.items():
            if game in games:
                platforms.append(platform)
        return platforms
    
    def _generate_reasoning(self, age: int, preferred_genres: List[str], recommendations: List[Dict[str, any]]) -> str:
        """
        Генерирует обоснование рекомендаций
        
        Args:
            age: Возраст пользователя
            preferred_genres: Предпочитаемые жанры
            recommendations: Список рекомендаций
            
        Returns:
            Текстовое обоснование
        """
        reasoning_parts = []
        
        # Обоснование по возрасту
        reasoning_parts.append(f"Учитывая ваш возраст ({age} лет), я подобрал игры с возрастным рейтингом до {age} лет.")
        
        # Обоснование по жанрам
        if preferred_genres:
            genres_str = ", ".join(preferred_genres)
            reasoning_parts.append(f"Основываясь на ваших предпочтениях в жанрах ({genres_str}), я включил соответствующие игры.")
        
        # Информация о количестве рекомендаций
        if recommendations:
            reasoning_parts.append(f"Найдено {len(recommendations)} подходящих игр, отсортированных по релевантности.")
            
            # Информация о топ-рекомендации
            if recommendations:
                top_game = recommendations[0]
                reasoning_parts.append(f"Топ-рекомендация: {top_game['name']} ({top_game['genre']}) - релевантность {top_game['relevance_score']:.2f}")
        else:
            reasoning_parts.append("К сожалению, не удалось найти точных совпадений, поэтому предложены альтернативные варианты.")
        
        return " ".join(reasoning_parts)
    
    def get_alternative_recommendations(self, age: int, excluded_genres: List[str] = None) -> List[Dict[str, any]]:
        """
        Получает альтернативные рекомендации исключая определенные жанры
        
        Args:
            age: Возраст пользователя
            excluded_genres: Жанры для исключения
            
        Returns:
            Список альтернативных рекомендаций
        """
        if excluded_genres is None:
            excluded_genres = []
        
        all_genres = self.kb.get_all_genres()
        alternative_genres = [g for g in all_genres if g not in excluded_genres]
        
        return self.get_recommendations(age, alternative_genres)

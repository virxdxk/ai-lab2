"""
Система поддержки принятия решений для выбора видеоигр
Лабораторная работа №2

Основная программа с диалогом пользователя
"""

import sys
from typing import Dict, List
from game_knowledge_base import GameKnowledgeBase
from input_parser import InputParser
from recommendation_engine import RecommendationEngine

class GameRecommendationSystem:
    def __init__(self):
        """Инициализация системы рекомендаций"""
        self.kb = GameKnowledgeBase()
        self.parser = InputParser()
        self.engine = RecommendationEngine(self.kb)
        self.session_data = {}
    
    def print_welcome(self):
        """Выводит приветственное сообщение"""
        print("=" * 60)
        print("СИСТЕМА РЕКОМЕНДАЦИЙ ВИДЕОИГР")
        print("=" * 60)
        print("Добро пожаловать в систему поддержки принятия решений!")
        print("Я помогу вам выбрать подходящие видеоигры на основе")
        print("вашего возраста и предпочтений в жанрах.")
        print()
        print("Доступные жанры:", ", ".join(self.kb.get_all_genres()))
        print()
    
    def print_examples(self):
        """Выводит примеры правильного ввода"""
        print("ПРИМЕРЫ ПРАВИЛЬНОГО ВВОДА:")
        print("-" * 40)
        examples = self.parser.get_parsing_examples()
        for i, example in enumerate(examples, 1):
            print(f"{i}. {example}")
        print()
    
    def get_user_input(self) -> str:
        """Получает ввод от пользователя"""
        print("Введите информацию о себе:")
        print("(укажите возраст и предпочитаемые жанры)")
        print("Пример: Мне 13 лет, мне нравятся: RPG, инди-игры")
        print()
        
        while True:
            try:
                user_input = input(">>> ").strip()
                if user_input.lower() in ['выход', 'exit', 'quit', 'q']:
                    return 'exit'
                if user_input:
                    return user_input
                else:
                    print("Пожалуйста, введите непустую строку.")
            except KeyboardInterrupt:
                print("\nДо свидания!")
                sys.exit(0)
            except EOFError:
                print("\nДо свидания!")
                sys.exit(0)
    
    def parse_and_validate_input(self, user_input: str) -> Dict[str, any]:
        """Парсит и валидирует ввод пользователя"""
        print("Анализирую ваш ввод...")
        
        # Парсим ввод
        parsed_data = self.parser.parse_input(user_input)
        
        # Валидируем данные
        validated_data = self.parser.validate_input(parsed_data)
        
        # Выводим результаты парсинга
        self._print_parsing_results(validated_data)
        
        return validated_data
    
    def _print_parsing_results(self, data: Dict[str, any]):
        """Выводит результаты парсинга"""
        print(f"РЕЗУЛЬТАТЫ АНАЛИЗА:")
        print(f"   Возраст: {data['age'] if data['age'] else 'не найден'}")
        print(f"   Жанры: {', '.join(data['genres']) if data['genres'] else 'не найдены'}")
        
        if not data['is_valid']:
            print("Ошибки:")
            if not data['age_valid']:
                print(f"   - {data['age_error']}")
            if not data['genres_valid']:
                print(f"   - {data['genres_error']}")
        else:
            print("Данные успешно обработаны!")
        print()
    
    def get_recommendations(self, age: int, genres: List[str]) -> Dict[str, any]:
        """Получает рекомендации от движка"""
        print("Ищу подходящие игры...")
        print("   Выполняю логические запросы к базе знаний...")
        
        recommendations = self.engine.get_recommendations(age, genres)
        
        print(f"Найдено {recommendations['total_found']} рекомендаций")
        print()
        
        return recommendations
    
    def display_recommendations(self, recommendations: Dict[str, any]):
        """Отображает рекомендации пользователю"""
        print("РЕКОМЕНДАЦИИ ИГР:")
        print("=" * 50)
        
        if not recommendations['recommendations']:
            print("К сожалению, не удалось найти подходящих игр.")
            print("Попробуйте изменить критерии поиска.")
            return
        
        # Выводим топ-5 рекомендаций
        top_recommendations = recommendations['recommendations'][:5]
        
        for i, game in enumerate(top_recommendations, 1):
            print(f"{i}. {game['name']}")
            print(f"   Жанр: {game['genre']}")
            print(f"   Возрастной рейтинг: {game['age_rating']}+")
            print(f"   Релевантность: {game['relevance_score']:.2f}")
            print(f"   Платформы: {', '.join(game['platforms'])}")
            print()
        
        # Выводим обоснование
        print("ОБОСНОВАНИЕ РЕКОМЕНДАЦИЙ:")
        print("-" * 40)
        print(recommendations['reasoning'])
        print()
    
    def ask_for_alternatives(self, age: int, current_genres: List[str]) -> bool:
        """Спрашивает пользователя о альтернативных рекомендациях"""
        print("Хотите получить альтернативные рекомендации?")
        print("(игры из других жанров)")
        
        while True:
            try:
                response = input(">>> ").strip().lower()
                if response in ['да', 'yes', 'y', 'д']:
                    return True
                elif response in ['нет', 'no', 'n', 'н']:
                    return False
                else:
                    print("Пожалуйста, ответьте 'да' или 'нет'.")
            except (KeyboardInterrupt, EOFError):
                return False
    
    def get_alternative_recommendations(self, age: int, current_genres: List[str]):
        """Получает и отображает альтернативные рекомендации"""
        print("Ищу альтернативные варианты...")
        
        alternatives = self.engine.get_alternative_recommendations(age, current_genres)
        
        if alternatives['recommendations']:
            print("АЛЬТЕРНАТИВНЫЕ РЕКОМЕНДАЦИИ:")
            print("=" * 50)
            
            top_alternatives = alternatives['recommendations'][:3]
            
            for i, game in enumerate(top_alternatives, 1):
                print(f"{i}. {game['name']}")
                print(f"   Жанр: {game['genre']}")
                print(f"   Возрастной рейтинг: {game['age_rating']}+")
                print(f"   Релевантность: {game['relevance_score']:.2f}")
                print()
        else:
            print("Альтернативные рекомендации не найдены.")
        print()
    
    def ask_for_continuation(self) -> bool:
        """Спрашивает пользователя о продолжении работы"""
        print("Хотите получить новые рекомендации?")
        
        while True:
            try:
                response = input(">>> ").strip().lower()
                if response in ['да', 'yes', 'y', 'д']:
                    return True
                elif response in ['нет', 'no', 'n', 'н']:
                    return False
                else:
                    print("Пожалуйста, ответьте 'да' или 'нет'.")
            except (KeyboardInterrupt, EOFError):
                return False
    
    def run(self):
        """Основной цикл работы системы"""
        self.print_welcome()
        self.print_examples()
        
        while True:
            try:
                # Получаем ввод пользователя
                user_input = self.get_user_input()
                
                if user_input == 'exit':
                    print("До свидания!")
                    break
                
                # Парсим и валидируем ввод
                parsed_data = self.parse_and_validate_input(user_input)
                
                if not parsed_data['is_valid']:
                    print("Не удалось обработать ввод. Попробуйте еще раз.")
                    print("Используйте примеры выше для правильного формата.")
                    print()
                    continue
                
                # Получаем рекомендации
                recommendations = self.get_recommendations(
                    parsed_data['age'], 
                    parsed_data['genres']
                )
                
                # Отображаем рекомендации
                self.display_recommendations(recommendations)
                
                # Предлагаем альтернативы
                if self.ask_for_alternatives(parsed_data['age'], parsed_data['genres']):
                    self.get_alternative_recommendations(parsed_data['age'], parsed_data['genres'])
                
                # Спрашиваем о продолжении
                if not self.ask_for_continuation():
                    print("Спасибо за использование системы! До свидания!")
                    break
                
                print("\n" + "="*60 + "\n")
                
            except Exception as e:
                print(f"Произошла ошибка: {e}")
                print("Попробуйте еще раз.")
                print()

def main():
    """Точка входа в программу"""
    try:
        system = GameRecommendationSystem()
        system.run()
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

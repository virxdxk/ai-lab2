"""
Тесты для системы рекомендаций видеоигр
Проверяет корректность работы всех компонентов системы
"""

import unittest
from game_knowledge_base import GameKnowledgeBase
from input_parser import InputParser
from recommendation_engine import RecommendationEngine

class TestGameKnowledgeBase(unittest.TestCase):
    """Тесты для базы знаний о играх"""
    
    def setUp(self):
        """Настройка тестов"""
        self.kb = GameKnowledgeBase()
    
    def test_get_games_by_genre(self):
        """Тест получения игр по жанру"""
        rpg_games = self.kb.get_games_by_genre('RPG')
        self.assertIsInstance(rpg_games, list)
        self.assertGreater(len(rpg_games), 0)
        self.assertIn('The Witcher 3', rpg_games)
        
        # Тест несуществующего жанра
        unknown_games = self.kb.get_games_by_genre('UnknownGenre')
        self.assertEqual(unknown_games, [])
    
    def test_get_games_by_age(self):
        """Тест получения игр по возрасту"""
        # Игры для 13-летнего
        games_13 = self.kb.get_games_by_age(13)
        self.assertIsInstance(games_13, list)
        self.assertGreater(len(games_13), 0)
        
        # Игры для 18-летнего (должно быть больше)
        games_18 = self.kb.get_games_by_age(18)
        self.assertGreaterEqual(len(games_18), len(games_13))
        
        # Проверяем, что все игры подходят по возрасту
        for game in games_13:
            age_rating = self.kb.get_game_age_rating(game)
            self.assertLessEqual(age_rating, 13)
    
    def test_get_game_genre(self):
        """Тест получения жанра игры"""
        genre = self.kb.get_game_genre('The Witcher 3')
        self.assertEqual(genre, 'RPG')
        
        # Тест несуществующей игры
        unknown_genre = self.kb.get_game_genre('Unknown Game')
        self.assertIsNone(unknown_genre)
    
    def test_get_game_age_rating(self):
        """Тест получения возрастного рейтинга"""
        age_rating = self.kb.get_game_age_rating('The Witcher 3')
        self.assertEqual(age_rating, 18)
        
        # Тест несуществующей игры
        unknown_rating = self.kb.get_game_age_rating('Unknown Game')
        self.assertEqual(unknown_rating, 18)  # По умолчанию 18+
    
    def test_get_all_genres(self):
        """Тест получения всех жанров"""
        genres = self.kb.get_all_genres()
        self.assertIsInstance(genres, list)
        self.assertGreater(len(genres), 0)
        self.assertIn('RPG', genres)
        self.assertIn('Action', genres)
    
    def test_get_all_games(self):
        """Тест получения всех игр"""
        games = self.kb.get_all_games()
        self.assertIsInstance(games, list)
        self.assertGreater(len(games), 0)
        self.assertIn('The Witcher 3', games)

class TestInputParser(unittest.TestCase):
    """Тесты для парсера входных данных"""
    
    def setUp(self):
        """Настройка тестов"""
        self.parser = InputParser()
    
    def test_parse_age(self):
        """Тест парсинга возраста"""
        test_cases = [
            ("Мне 13 лет, мне нравятся: RPG", 13),
            ("Возраст: 25, люблю Action", 25),
            ("Я 18 лет, интересы: Horror", 18),
            ("Мне 30 лет, предпочтения: Simulation", 30),
            ("Возраст 16, нравятся Racing", 16)
        ]
        
        for input_text, expected_age in test_cases:
            with self.subTest(input=input_text):
                parsed = self.parser.parse_input(input_text)
                self.assertEqual(parsed['age'], expected_age)
    
    def test_parse_genres(self):
        """Тест парсинга жанров"""
        test_cases = [
            ("Мне 13 лет, мне нравятся: RPG, инди-игры", ['RPG', 'Indie']),
            ("Возраст: 25, люблю Action и Strategy", ['Action', 'Strategy']),
            ("Я 18 лет, интересы: Horror, Adventure", ['Horror', 'Adventure']),
            ("Мне 30 лет, предпочтения: Simulation, Puzzle", ['Simulation', 'Puzzle']),
            ("Возраст 16, нравятся Racing и Sports", ['Racing', 'Sports'])
        ]
        
        for input_text, expected_genres in test_cases:
            with self.subTest(input=input_text):
                parsed = self.parser.parse_input(input_text)
                # Проверяем, что все ожидаемые жанры найдены
                for genre in expected_genres:
                    self.assertIn(genre, parsed['genres'])
    
    def test_parse_invalid_input(self):
        """Тест парсинга некорректного ввода"""
        invalid_inputs = [
            "Привет, как дела?",
            "Мне нравятся игры",
            "Возраст: старый",
            ""
        ]
        
        for invalid_input in invalid_inputs:
            with self.subTest(input=invalid_input):
                parsed = self.parser.parse_input(invalid_input)
                validated = self.parser.validate_input(parsed)
                self.assertFalse(validated['is_valid'])
    
    def test_validate_input(self):
        """Тест валидации ввода"""
        # Корректный ввод
        valid_input = "Мне 13 лет, мне нравятся: RPG, инди-игры"
        parsed = self.parser.parse_input(valid_input)
        validated = self.parser.validate_input(parsed)
        self.assertTrue(validated['is_valid'])
        self.assertTrue(validated['age_valid'])
        self.assertTrue(validated['genres_valid'])
        
        # Некорректный ввод
        invalid_input = "Привет"
        parsed = self.parser.parse_input(invalid_input)
        validated = self.parser.validate_input(parsed)
        self.assertFalse(validated['is_valid'])
        self.assertFalse(validated['age_valid'])
        self.assertFalse(validated['genres_valid'])

class TestRecommendationEngine(unittest.TestCase):
    """Тесты для движка рекомендаций"""
    
    def setUp(self):
        """Настройка тестов"""
        self.kb = GameKnowledgeBase()
        self.engine = RecommendationEngine(self.kb)
    
    def test_get_recommendations(self):
        """Тест получения рекомендаций"""
        recommendations = self.engine.get_recommendations(13, ['RPG', 'Indie'])
        
        self.assertIsInstance(recommendations, dict)
        self.assertIn('recommendations', recommendations)
        self.assertIn('reasoning', recommendations)
        self.assertIn('total_found', recommendations)
        
        # Проверяем структуру рекомендаций
        for rec in recommendations['recommendations']:
            self.assertIn('name', rec)
            self.assertIn('genre', rec)
            self.assertIn('age_rating', rec)
            self.assertIn('relevance_score', rec)
            self.assertIn('platforms', rec)
    
    def test_age_appropriate_filtering(self):
        """Тест фильтрации по возрасту"""
        # Для 13-летнего не должно быть игр 18+
        recommendations = self.engine.get_recommendations(13, ['Action'])
        
        for rec in recommendations['recommendations']:
            self.assertLessEqual(rec['age_rating'], 13)
    
    def test_genre_matching(self):
        """Тест соответствия жанрам"""
        recommendations = self.engine.get_recommendations(18, ['RPG'])
        
        # Все рекомендации должны быть RPG или иметь высокую релевантность
        rpg_found = False
        for rec in recommendations['recommendations']:
            if rec['genre'] == 'RPG':
                rpg_found = True
                break
        
        # Если есть RPG игры в базе, они должны быть найдены
        rpg_games = self.kb.get_games_by_genre('RPG')
        if rpg_games:
            self.assertTrue(rpg_found)
    
    def test_relevance_scoring(self):
        """Тест системы оценки релевантности"""
        recommendations = self.engine.get_recommendations(18, ['RPG'])
        
        # Проверяем, что оценки релевантности в правильном диапазоне
        for rec in recommendations['recommendations']:
            self.assertGreaterEqual(rec['relevance_score'], 0.0)
            self.assertLessEqual(rec['relevance_score'], 1.0)
        
        # Проверяем, что рекомендации отсортированы по убыванию релевантности
        scores = [rec['relevance_score'] for rec in recommendations['recommendations']]
        self.assertEqual(scores, sorted(scores, reverse=True))
    
    def test_alternative_recommendations(self):
        """Тест альтернативных рекомендаций"""
        alternatives = self.engine.get_alternative_recommendations(18, ['RPG'])
        
        self.assertIsInstance(alternatives, dict)
        self.assertIn('recommendations', alternatives)
        
        # Альтернативные рекомендации не должны содержать RPG
        for rec in alternatives['recommendations']:
            self.assertNotEqual(rec['genre'], 'RPG')

class TestSystemIntegration(unittest.TestCase):
    """Интеграционные тесты всей системы"""
    
    def setUp(self):
        """Настройка тестов"""
        self.kb = GameKnowledgeBase()
        self.parser = InputParser()
        self.engine = RecommendationEngine(self.kb)
    
    def test_full_workflow(self):
        """Тест полного рабочего процесса"""
        # Тестовый ввод
        user_input = "Мне 13 лет, мне нравятся: RPG, инди-игры"
        
        # Парсинг
        parsed = self.parser.parse_input(user_input)
        validated = self.parser.validate_input(parsed)
        
        self.assertTrue(validated['is_valid'])
        self.assertEqual(validated['age'], 13)
        self.assertIn('RPG', validated['genres'])
        self.assertIn('Indie', validated['genres'])
        
        # Получение рекомендаций
        recommendations = self.engine.get_recommendations(
            validated['age'], 
            validated['genres']
        )
        
        self.assertIsInstance(recommendations, dict)
        self.assertGreater(recommendations['total_found'], 0)
        
        # Проверяем, что все рекомендации подходят по возрасту
        for rec in recommendations['recommendations']:
            self.assertLessEqual(rec['age_rating'], 13)
    
    def test_edge_cases(self):
        """Тест граничных случаев"""
        # Очень молодой возраст
        recommendations = self.engine.get_recommendations(3, ['Puzzle'])
        self.assertIsInstance(recommendations, dict)
        
        # Очень старый возраст
        recommendations = self.engine.get_recommendations(100, ['Strategy'])
        self.assertIsInstance(recommendations, dict)
        
        # Несуществующие жанры
        recommendations = self.engine.get_recommendations(18, ['UnknownGenre'])
        self.assertIsInstance(recommendations, dict)
        
        # Пустой список жанров
        recommendations = self.engine.get_recommendations(18, [])
        self.assertIsInstance(recommendations, dict)

def run_tests():
    """Запуск всех тестов"""
    print("Запуск тестов системы рекомендаций игр...")
    print("=" * 60)
    
    # Создаем тестовый набор
    test_suite = unittest.TestSuite()
    
    # Добавляем тесты
    test_classes = [
        TestGameKnowledgeBase,
        TestInputParser,
        TestRecommendationEngine,
        TestSystemIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Выводим результаты
    print("\n" + "=" * 60)
    print(f"РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print(f"   Всего тестов: {result.testsRun}")
    print(f"   Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"   Ошибок: {len(result.failures)}")
    print(f"   Исключений: {len(result.errors)}")
    
    if result.failures:
        print("\nНЕУДАЧНЫЕ ТЕСТЫ:")
        for test, traceback in result.failures:
            print(f"   - {test}: {traceback}")
    
    if result.errors:
        print("\nОШИБКИ В ТЕСТАХ:")
        for test, traceback in result.errors:
            print(f"   - {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\nВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")
        return True
    else:
        print("\nНЕКОТОРЫЕ ТЕСТЫ НЕ ПРОШЛИ!")
        return False

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)

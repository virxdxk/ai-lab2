"""
База знаний о видеоиграх для системы рекомендаций
Содержит факты о играх, жанрах, возрастных ограничениях и правила для рекомендаций
"""

class GameKnowledgeBase:
    def __init__(self):
        # Факты о жанрах игр
        self.genres = {
            'RPG': ['The Witcher 3', 'Skyrim', 'Final Fantasy XV', 'Persona 5', 'Divinity: Original Sin 2'],
            'Action': ['Grand Theft Auto V', 'Assassin\'s Creed Valhalla', 'Call of Duty: Modern Warfare', 'Cyberpunk 2077'],
            'Adventure': ['The Legend of Zelda: Breath of the Wild', 'Uncharted 4', 'Tomb Raider', 'Life is Strange'],
            'Strategy': ['Civilization VI', 'Total War: Warhammer III', 'Age of Empires IV', 'Crusader Kings III'],
            'Simulation': ['The Sims 4', 'Cities: Skylines', 'Euro Truck Simulator 2', 'Farming Simulator 22'],
            'Puzzle': ['Portal 2', 'Tetris Effect', 'The Witness', 'Baba is You'],
            'Indie': ['Hollow Knight', 'Celeste', 'Stardew Valley', 'Among Us', 'Cuphead'],
            'Horror': ['Resident Evil Village', 'Silent Hill', 'Outlast', 'Amnesia: The Dark Descent'],
            'Racing': ['Forza Horizon 5', 'Gran Turismo 7', 'Mario Kart 8', 'Need for Speed Heat'],
            'Sports': ['FIFA 23', 'NBA 2K23', 'Rocket League', 'Tony Hawk\'s Pro Skater 1+2']
        }
        
        # Факты о возрастных ограничениях игр
        self.age_ratings = {
            'The Witcher 3': 18,
            'Skyrim': 17,
            'Final Fantasy XV': 13,
            'Persona 5': 17,
            'Divinity: Original Sin 2': 17,
            'Grand Theft Auto V': 18,
            'Assassin\'s Creed Valhalla': 17,
            'Call of Duty: Modern Warfare': 17,
            'Cyberpunk 2077': 18,
            'The Legend of Zelda: Breath of the Wild': 10,
            'Uncharted 4': 13,
            'Tomb Raider': 17,
            'Life is Strange': 13,
            'Civilization VI': 10,
            'Total War: Warhammer III': 16,
            'Age of Empires IV': 10,
            'Crusader Kings III': 16,
            'The Sims 4': 12,
            'Cities: Skylines': 10,
            'Euro Truck Simulator 2': 3,
            'Farming Simulator 22': 3,
            'Portal 2': 10,
            'Tetris Effect': 3,
            'The Witness': 10,
            'Baba is You': 3,
            'Hollow Knight': 10,
            'Celeste': 10,
            'Stardew Valley': 10,
            'Among Us': 10,
            'Cuphead': 10,
            'Resident Evil Village': 18,
            'Silent Hill': 17,
            'Outlast': 18,
            'Amnesia: The Dark Descent': 17,
            'Forza Horizon 5': 3,
            'Gran Turismo 7': 3,
            'Mario Kart 8': 3,
            'Need for Speed Heat': 13,
            'FIFA 23': 3,
            'NBA 2K23': 3,
            'Rocket League': 3,
            'Tony Hawk\'s Pro Skater 1+2': 10
        }
        
        # Факты о сложности игр
        self.difficulty = {
            'easy': ['The Sims 4', 'Cities: Skylines', 'Stardew Valley', 'Mario Kart 8', 'FIFA 23', 'Rocket League'],
            'medium': ['Skyrim', 'The Legend of Zelda: Breath of the Wild', 'Uncharted 4', 'Civilization VI', 'Hollow Knight'],
            'hard': ['The Witcher 3', 'Dark Souls', 'Cuphead', 'Celeste', 'Total War: Warhammer III']
        }
        
        # Факты о популярности игр
        self.popularity = {
            'very_popular': ['The Witcher 3', 'Grand Theft Auto V', 'Minecraft', 'Among Us', 'Rocket League'],
            'popular': ['Skyrim', 'The Legend of Zelda: Breath of the Wild', 'Stardew Valley', 'Hollow Knight'],
            'niche': ['Divinity: Original Sin 2', 'Crusader Kings III', 'The Witness', 'Baba is You']
        }
        
        # Факты о платформах
        self.platforms = {
            'PC': ['The Witcher 3', 'Skyrim', 'Civilization VI', 'Cities: Skylines', 'Portal 2', 'Hollow Knight'],
            'PlayStation': ['The Witcher 3', 'Skyrim', 'Uncharted 4', 'Gran Turismo 7', 'Persona 5'],
            'Xbox': ['The Witcher 3', 'Skyrim', 'Forza Horizon 5', 'Halo Infinite', 'Gears 5'],
            'Nintendo': ['The Legend of Zelda: Breath of the Wild', 'Mario Kart 8', 'Super Mario Odyssey'],
            'Mobile': ['Among Us', 'Candy Crush Saga', 'Clash of Clans', 'Pokemon GO']
        }
    
    def get_games_by_genre(self, genre):
        """Получить игры по жанру"""
        return self.genres.get(genre, [])
    
    def get_games_by_age(self, age):
        """Получить игры подходящие по возрасту"""
        suitable_games = []
        for game, min_age in self.age_ratings.items():
            if min_age <= age:
                suitable_games.append(game)
        return suitable_games
    
    def get_games_by_difficulty(self, difficulty_level):
        """Получить игры по уровню сложности"""
        return self.difficulty.get(difficulty_level, [])
    
    def get_games_by_popularity(self, popularity_level):
        """Получить игры по уровню популярности"""
        return self.popularity.get(popularity_level, [])
    
    def get_game_genre(self, game):
        """Получить жанр игры"""
        for genre, games in self.genres.items():
            if game in games:
                return genre
        return None
    
    def get_game_age_rating(self, game):
        """Получить возрастной рейтинг игры"""
        return self.age_ratings.get(game, 18)
    
    def get_all_genres(self):
        """Получить все доступные жанры"""
        return list(self.genres.keys())
    
    def get_all_games(self):
        """Получить все игры"""
        all_games = set()
        for games in self.genres.values():
            all_games.update(games)
        return list(all_games)

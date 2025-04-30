import random
import unittest
from io import StringIO
import sys
from unittest.mock import patch



def generate_random_number(min_val, max_val):
    """Генерация случайного числа в заданном диапазоне"""
    return random.randint(min_val, max_val)

def validate_input(user_input, min_val, max_val):
    """Проверка корректности ввода пользователя"""
    try:
        num = int(user_input)
        return min_val <= num <= max_val
    except ValueError:
        return False

def get_user_guess(attempt, min_num, max_num):
    """Получение и проверка числа от пользователя"""
    while True:
        try:
            guess = int(input(f"Попытка {attempt}. Введите ваше число: "))
            if guess < min_num or guess > max_num:
                print(f"Число должно быть в диапазоне от {min_num} до {max_num}.")
            else:
                return guess
        except ValueError:
            print("Пожалуйста, введите целое число.")

def game_round(min_num, max_num, max_attempts):
    """Один раунд игры"""
    secret_number = generate_random_number(min_num, max_num)
    attempts = 0
    
    while attempts < max_attempts:
        attempts += 1
        remaining = max_attempts - attempts
        
        guess = get_user_guess(attempts, min_num, max_num)
        
        if guess < secret_number:
            print("Больше")
            if remaining > 0:
                print(f"Осталось попыток: {remaining}")
        elif guess > secret_number:
            print("Меньше")
            if remaining > 0:
                print(f"Осталось попыток: {remaining}")
        else:
            print(f"Угадал! Это число {secret_number}.")
            print(f"Вы угадали за {attempts} попыток.")
            return True
    
    print(f"Закончились шаги. Загаданное число было: {secret_number}.")
    return False

def main():
    """Основная функция игры"""
    print("Добро пожаловать в игру 'Угадай число'!")
    
    while True:

        while True:
            try:
                min_num = int(input("Введите нижнюю границу диапазона: "))
                max_num = int(input("Введите верхнюю границу диапазона: "))
                if min_num >= max_num:
                    print("Верхняя граница должна быть больше нижней. Попробуйте снова.")
                else:
                    break
            except ValueError:
                print("Пожалуйста, введите целое число.")
        

        while True:
            try:
                max_attempts = int(input(f"За сколько шагов вы сможете угадать число от {min_num} до {max_num}? "))
                if max_attempts <= 0:
                    print("Количество шагов должно быть положительным числом.")
                else:
                    break
            except ValueError:
                print("Пожалуйста, введите целое число.")
        

        game_round(min_num, max_num, max_attempts)
        

        play_again = input("Хотите сыграть снова? (да/нет): ").lower()
        if play_again not in ['да', 'д', 'yes', 'y']:
            print("Спасибо за игру! До свидания!")
            break



class TestGuessNumberGame(unittest.TestCase):
    """Полная система тестов для игры 'Угадай число'"""
    

    def test_random_number_generation(self):
        for _ in range(100):
            num = generate_random_number(1, 100)
            self.assertTrue(1 <= num <= 100)
    

    def test_input_validation(self):
        self.assertTrue(validate_input("50", 1, 100))
        self.assertFalse(validate_input("abc", 1, 100))
        self.assertFalse(validate_input("150", 1, 100))
    

    @patch('builtins.input', side_effect=['50'])
    @patch('random.randint', return_value=50)
    def test_win_first_try(self, mock_randint, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = game_round(1, 100, 5)
            self.assertTrue(result)
            self.assertIn("Угадал!", fake_out.getvalue())
    
    @patch('builtins.input', side_effect=['50', '75', '25'])
    @patch('random.randint', return_value=60)
    def test_lose_game(self, mock_randint, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = game_round(1, 100, 3)
            self.assertFalse(result)
            self.assertIn("Закончились шаги", fake_out.getvalue())
    

    @patch('builtins.input', side_effect=['1', '100', '5', '50', '75', '60', 'нет'])
    @patch('random.randint', return_value=60)
    def test_full_game_flow(self, mock_randint, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()
            self.assertIn("Добро пожаловать", output)
            self.assertIn("Угадал!", output)
            self.assertIn("Спасибо за игру", output)



if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=['first-arg-is-ignored'])
    else:
        main()
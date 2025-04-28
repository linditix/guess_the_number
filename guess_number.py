import random

def guess_number_game():
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
                print("Пожалуйста, введите целые числа.")
        
        secret_number = random.randint(min_num, max_num)
        
        while True:
            try:
                max_attempts = int(input(f"За сколько шагов вы сможете угадать число от {min_num} до {max_num}? "))
                if max_attempts <= 0:
                    print("Количество шагов должно быть положительным числом.")
                else:
                    break
            except ValueError:
                print("Пожалуйста, введите целое число.")
        
        print(f"Попробуйте угадать число от {min_num} до {max_num}!")
        
        attempts = 0
        guessed = False
        
        while attempts < max_attempts and not guessed:
            attempts += 1
            remaining_attempts = max_attempts - attempts
            
            while True:
                try:
                    guess = int(input(f"Попытка {attempts}. Введите ваше число: "))
                    if guess < min_num or guess > max_num:
                        print(f"Число должно быть в диапазоне от {min_num} до {max_num}.")
                    else:
                        break
                except ValueError:
                    print("Пожалуйста, введите целое число.")
            
            if guess < secret_number:
                print("Больше")
                if remaining_attempts > 0:
                    print(f"Осталось попыток: {remaining_attempts}")
            elif guess > secret_number:
                print("Меньше")
                if remaining_attempts > 0:
                    print(f"Осталось попыток: {remaining_attempts}")
            else:
                print(f"Угадал! Это число {secret_number}.")
                print(f"Вы угадали за {attempts} попыток.")
                guessed = True
        
        if not guessed:
            print(f"Закончились шаги. Загаданное число было: {secret_number}.")
        
        play_again = input("Хотите сыграть снова? (да/нет): ").lower()
        if play_again not in ['да', 'д', 'yes', 'y']:
            print("Спасибо за игру! До свидания!")
            break

if __name__ == "__main__":
    guess_number_game()
import random

def game(secret_numb=random.randint(1, 10),up_range=10, times=4, smart_random=False):
    count = 1
    while count < times:
        if smart_random:
            secret_numb = random.randint(1, up_range)
            print("Secret number: ", secret_numb)
            print()
        try:
            guess = int(input(f'Attempt {count}. Guess the number:\n'))
        except:
            print(f'\nError! Try number type between 1 and {up_range}...\n')
        else:
            if guess >= 1 and guess <= up_range:
                if guess > secret_numb:
                    print('\nYour number is bigger!\n')
                elif guess < secret_numb:
                    print('\nYour number is lower!\n')
                else:
                    return '\nYou win!'
                count += 1
            else:
                print(f'\nError! Try number between 1 and {up_range}...\n')
    return 'You lose!'

print(game())
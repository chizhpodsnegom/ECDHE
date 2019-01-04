#! python3

from hashlib import sha224
from collections import namedtuple
from random import randint
import json
from re import fullmatch
import os
import matplotlib.pyplot as plot


# Задание эллиптической кривой и ее параметров
EllipticCurve = namedtuple('EllipticCurve', ['p', 'a', 'b', 'g'])

curve = EllipticCurve(
    # Field characteristic
    p=31991,
    # Curve characteristic
    a=31998,
    b=1000,
    g=[0, 5585]
)


# Возвращает обратный по модулю, если (b,a) = 1; # b - модуль
def xgcd(b, a):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return y0


# Сложение точки с собой k раз; x, y в формате *[,,]
def multiply(ec_point, k, module=31991, x_axis=[], y_axis=[]):
    x1, y1 = ec_point
    x2, y2 = ec_point
    # результат
    d3 = ['None', 'None']

    if x_axis != [] and y_axis != []:
        for i in range(k - 1):

            if x1 == x2 and y1 == y2:
                la = ((3 * x1 ** 2 + 31988) * xgcd(module, (2 * y1) % module)) % module
            else:
                la = ((y2 - y1) * xgcd(module, (x2 - x1) % module)) % module
            d3[0] = (la ** 2 - x1 - x2) % module
            d3[1] = (la * (x1 - d3[0]) - y1) % module

            x1, y1 = d3[0], d3[1]

            x_axis.append(x1)
            y_axis.append(y1)
    else:
        for i in range(k - 1):

            if x1 == x2 and y1 == y2:
                la = ((3 * x1 ** 2 + 31988) * xgcd(module, (2 * y1) % module)) % module
            else:
                la = ((y2 - y1) * xgcd(module, (x2 - x1) % module)) % module
            d3[0] = (la ** 2 - x1 - x2) % module
            d3[1] = (la * (x1 - d3[0]) - y1) % module

            x1, y1 = d3[0], d3[1]
        return d3


# Функция регистрации пользователей по паролю
def signup():
    print('''Write your password below
    It must be at least 5 characters(max 20)
    and only letters, digits and underscore sign "_" are allowed:''')

    passwd = input()
    match = fullmatch(r'\w{5,20}', passwd)
    if not match:
        return print('This password is incorrect, please try to /signup again')

    if os.path.isfile('shadow.json'):
        shadow = open('shadow.json', 'r')
        dictionary = json.loads(shadow.read())

        shadow = open('shadow.json', 'w')

        dictionary.update({"%i" % (len(dictionary) + 1): sha224(passwd.encode('utf-8')).hexdigest()})
        shadow.write(json.dumps(dictionary, sort_keys=True, indent=4))
        shadow.close()
    else:
        shadow = open('shadow.json', 'w')
        shadow.write(json.dumps({"1": sha224(passwd.encode('utf-8')).hexdigest()}, indent=4))
        shadow.close()

    return print('Your password is added')


# Функция очистки файла shadow.json
def delete():
    if os.path.isfile('shadow.json'):
        os.remove('shadow.json')
        return print('File shadow.json is deleted successfully')
    else:
        return print('No such file')


# Функция навигации по программе
def helpme():
    print('''
    Hello, %username%
    This is the ECDHE common key generator
    If you get stuck, use following commands:
    /helpme - see this message again :)
    /signup - register yourself in the system
    /signin - log in with password
    /delete  - clean up shadow.json
    /exit   - say goodbye
    ''')


# Функция входа в систему
def signin():
    print('Print you password to log in')
    passwd_check = input()

    try:
        with open('shadow.json', 'r') as shadow:
            result = shadow.read()
        if not result:
            raise Exception('file shadow.json is empty')
        else:
            passwd_dict = json.loads(result)

            match = False

            for i in range(1, len(passwd_dict) + 1):

                if sha224(passwd_check.encode('utf-8')).hexdigest() == passwd_dict[str(i)]:
                    print('OK, initialization of DH key generation')
                    match = True
                    dh_key()

            if not match:
                return print('Not such password in system memory')

    except IOError:
        print('file shadow.json is not exist')
    except Exception as e:
        print(e)


# Функция генерации ключа
def dh_key():
    print('ECDHE algorithm is working')

    private_key_a = randint(1, curve.p)
    private_key_b = randint(1, curve.p)

    key_a_g = multiply(curve.g, private_key_a, curve.p)
    key_b_g = multiply(curve.g, private_key_b, curve.p)

    key_a_key_b_g = multiply(key_a_g, private_key_b, curve.p)
    key_b_key_a_g = multiply(key_b_g, private_key_a, curve.p)

    table = '''
     /User-----------/private part(Ka,Kb)/public part(KaG,KbG)/common key(KaKbG)/
     |_______________|___________________|___________________|__________________|
     |UserA          |%i                 |%i,%i    |(%i,%i)      |
     |UserB          |%i                 |%i,%i    |(%i,%i)      |''' % (private_key_a, key_a_g[0],
                                                                         key_a_g[1], key_a_key_b_g[0],
                                                                         key_a_key_b_g[1], private_key_b,
                                                                         key_b_g[0], key_b_g[1],
                                                                         key_b_key_a_g[0], key_b_key_a_g[1])
    print(table)

    x_axis, y_axis = [key_a_g[0]], [key_a_g[1]]
    multiply(key_a_g, private_key_b, curve.p, x_axis, y_axis, )

    plot.scatter(x_axis, y_axis)  # scatter - метод для нанесения маркера в точке
    plot.title('Elliptic curve points from (%i,%i) to (%i,%i)' % (key_a_g[0], key_a_g[1],
                                                                  key_a_key_b_g[0], key_a_key_b_g[1]))
    plot.ylabel('y')
    plot.xlabel('x')

    plot.show()


print('''
Elliptic curve Diffie - Hellman common key generation
********* For more information use /helpme ************
''')

user_input = 0
while user_input != '/exit':
    if user_input == '/signin':
        signin()
    elif user_input == '/signup':
        signup()
    elif user_input == '/helpme':
        helpme()
    elif user_input == '/delete':
        delete()

    print('listening...')
    user_input = input()

print('\nGoodbye')

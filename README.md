# ECDHE
Elliptic curve Diffie - Hellman ephemeral protocol with authorization

Программа для генерации общего секретного ключа по протоколу
Диффи-Хеллмана на эллиптических кривых.

Работа программы:
после запуска ecdhe.py программа пребывает в режиме ожидания (listening) ввода от пользователя одной из комманд:
/helpme - вывод списка всех комманд и их действий
/signin - вход в систему через записанный в систему пароль и одновременный запуск протокола Диффи-Хеллмана
/signup - регистрация пользователя по паролю
/delete - удаление файла с паролями shadow.json
/exit - корректное завершение программы

После успешного входа в систему(/singup) выводится таблица в консоли с промежуточными данными, итоговым общим ключем,
а также график, на котором изображены промежуточные точки от KaG до KaKbG, их число зависит от Kb.

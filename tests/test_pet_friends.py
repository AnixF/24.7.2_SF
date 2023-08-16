from api import PetFriends
from settings import valid_email, valid_password
import os


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


# Новые 10 тестов
def test_add_new_pet_simple_with_valid_data(name='Барсик', animal_type='кот', age=3):
    """Проверяем возможность добавления питомца с простыми данными"""

    # Запрашиваем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца с простыми данными
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    print(result)
    # Сохраняем id питомца в переменную
    pet_id = result['id']

def test_add_pet_photo_with_valid_data(pet_id='12345', pet_photo='images/cat1.jpg'):
    """Проверяем возможность добавления фотографии питомца"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем id добавленного питомца
    create_pet_result = pf.create_pet_simple(auth_key, name='Барсик', animal_type='кот', age=3)
    pet_id = create_pet_result[1]['id']

    # Добавляем фотографию питомца
    status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)
    print(result)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert 'pet_photo' in result


def test_get_api_key_with_invalid_email(email='invalid_email', password=valid_password):
    """Проверяем реакцию при попытке получить api ключ с некорректным email"""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'Forbidden' in result


def test_get_all_pets_with_invalid_key(filter=''):
    """Проверяем реакцию при попытке получить список питомцев с некорректным ключом авторизации"""

    invalid_key = {"key" : 'invalid_key'}
    status, result = pf.get_list_of_pets(invalid_key, filter)

    print(status)
    assert status == 403
    #ssert 'error' in result



def test_add_new_pet_with_missing_parameters():
    """Проверяем реакцию при попытке добавить питомца с пропущенными параметрами"""

    name = ""
    animal_type = ""
    age = ""
    pet_photo = "images/cat1.jpg"

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200




def test_add_new_pet_with_large_age(name='Барсик', animal_type='99999', age="кот"):
    """Проверяем реакцию при попытке поменять местами вид животного и возраст"""

    pet_photo = 'images/cat1.jpg'

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400
    assert 'error' in result
    # Тест проваливается, недоработка сайта, возраста "кот" быть не должно


def test_update_pet_info_with_invalid_pet_id(name='Мурзик', animal_type='кот', age=5):
    """Проверяем реакцию при попытке обновить информацию о питомце с некорректным ID"""

    invalid_pet_id = 'invalid_id'

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.update_pet_info(auth_key, invalid_pet_id, name, animal_type, age)

    assert status == 400
    assert 'Bad Request' in result



def test_delete_pet_with_invalid_key(pet_id='12345'):
    """Проверяем реакцию при попытке удалить питомца с некорректным ключом авторизации"""

    invalid_key = {"key" : 'invalid_key'}

    status, _ = pf.delete_pet(invalid_key, pet_id)

    assert status == 403



def test_delete_pet_with_invalid_pet_id():
    """Проверяем реакцию при попытке удалить питомца с некорректным ID"""

    invalid_pet_id = 'invalid_id'

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.delete_pet(auth_key, invalid_pet_id)

    assert status == 404
    #тест проваливается, сайт не должен давать удалять несуществующего питомца, или должен хотя бы сообщить об удалении


def test_add_pet_photo_with_invalid_key(pet_id='12345', pet_photo='images/cat1.jpg'):
    """Проверяем реакцию при попытке добавить фотографию питомца с некорректным ключом авторизации"""

    invalid_key = {"key" : 'invalid_key'}

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    status, result = pf.add_pet_photo(invalid_key, pet_id, pet_photo)

    assert status == 403
    assert 'Forbidden' in result
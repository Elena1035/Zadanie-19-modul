import os
from api import PetFriends
from settings import valid_email, valid_password, invalid_password, invalid_email



pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

# Test 3
def test_get_api_key_correct_mail_and_wrong_passwor(email=valid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
     # """Верный емаил и неверный пароль"""
    assert status == 403
    assert 'key' not in result
    print('ok')
    print(f'Статус {status} для теста с неверным паролем')

# Test 4
def test_get_api_key_wrong_email_and_correct_password(email=invalid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    # """неверный емаил и верный пароль"""
    assert status == 403
    assert 'key' not in result
    print('ok')
    print(f'Статус {status} для теста с неверным email')

# Test 5
def test_get_api_key_with_wrong_email_and_wrong_password(email=invalid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
     # """Неверный емаил и неверный пароль"""
    assert status == 403
    assert 'key' not in result
    print('ok')
    print(f'Статус {status} для теста с неверными email и паролем')

# Test 6
def test_add_pet_valid_data_no_photo(name='Барбос_без_фото', animal_type='Кот', age='1'):
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    print('ok')
    print(f'добавлен {result}')

# Test 7
def test_add_photo_for_pet(pet_photo='images/123.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(api_key, my_pets['pets'][0]['id'], pet_photo)
        _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
        print(f'\n фото добавлено {result}')
    else:
        raise Exception('Питомцы отсутствуют')

# Test 8 добавление животного с пустыми полями
def test_add_pet_with_valid_data_empty_fields():
    name = ''
    animal_type = ''
    age = ''
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    print('ok')
    print(f'Сайт позволяет добавлять питомцев с пустыми полями {result}')

# Test 9
def test_delete_pet():
    # """удалить питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Мишутка", "кот", "2", "images/123.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Отправляем запрос на удаление первого питомца из списка
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Повторно запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

# Test 10
def test_add_pet_with_empty_value_in_variable_name(name='', animal_type='cat', age='2', pet_photo='images/koalla.jpg'):
    '''Проверяем возможность добавления питомца с пустым значением в переменной name
    Тест не будет пройден если питомец будет добавлен на сайт с пустым значением в поле "имя"'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] != '', 'Питомец добавлен на сайт с пустым значением в имени'











































































































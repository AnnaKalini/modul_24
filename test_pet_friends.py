from api import PetFriends

from settings import valid_email, valid_password, invalid_email, invalid_password


pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_api_key_for_invalid_email(email=invalid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 403 при невалидном email, но с валидным password"""
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_api_key_for_invalid_password(email=valid_email, password=invalid_password):
    """ Проверяем что запрос api ключа возвращает статус 403 при невалидном password, но с валидным email"""
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_get_all_pets_with_invalid_key(filter=''):
    """ Проверяем что нельзя запросить список всех питомцев при некорректном ключе авторизации"""
    auth_key = {"key": "incorrect"}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403

def test_add_new_pet_with_valid_data(name='Барсик', animal_type='метис', age='5', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    #pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_twice(name='Рыжик', animal_type='метис', age='3', pet_photo='images/cat1.jpg'):
    """Проверяем что нельзя создать две одинаковые карточки питомца в одном профиле"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400
    """Тест падает, т.к. сервис не осуществляет проверку на дубликаты карточек питомца в конкретном профиле."""

def test_add_new_pet_with_invalid_key(name='Барсик', animal_type='метис', age='5', pet_photo='images/cat1.jpg'):
    """Проверяем что нельзя добавить питомца при некорректном ключе авторизации"""
    auth_key = {"key": "incorrect"}
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 403

def test_add_new_pet_with_invalid_age(name='Барсик', animal_type='метис', age='-5', pet_photo='images/cat1.jpg'):
    """Проверяем что нельзя добавить питомца с отрицательным возрастом"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400
    """Тест падает, т.к. сервис не осуществляет проверку на ввод отрицательного числа. Поле age не валидируется и
    может принимать любые значения."""

def test_add_new_pet_without_photo_with_valid_data(name='Батон', animal_type='метис', age='3'):
    """Проверяем что можно создать карточку питомца без фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200

def test_add_new_pet_without_photo_with_invalid_data(name='', animal_type='', age=''):
    """Проверяем что нельзя создать карточку питомца, в которой не заполнено ни одно поле"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 400
    """Тест падает, т.к. сервис не валидирует поля name, animal_type, age"""

def test_add_new_pet_without_photo_with_invalid_key(name='Батон', animal_type='метис', age='3'):
    """Проверяем что нельзя создать карточку питомца без фото при некорректном ключе авторизации"""
    auth_key = {"key": "incorrect"}
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 403

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Сэм", "собака", "3", "images/orig(1).jpeg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Шарик', animal_type='овчарка', age=5):
    """Проверяем возможность обновления информации о питомце"""
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_successful_add_photo_of_pet(pet_photo='images/orig.jpeg'):
    """Проверяем возможность добавления фото к карточке питомца"""
    #pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем нового питомца без фото
    pf.add_new_pet_without_photo(auth_key, "Собака", "Шницель", "1")
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
    assert status == 200

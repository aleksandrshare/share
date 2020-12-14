import allure


class TestObj:
    @allure.epic('Int API')
    @allure.feature('Text')
    @allure.story('Создание obj')
    @allure.testcase('https://testrail.dom_name', 'TestCase link on TestRail')
    def test_create_new_alert(self, lko_admin):
        with allure.step('Отправляем запрос на создание obj'):
            alert_id, alert_data = lko_admin.aa_create_alert_with_random_fields()
        with allure.step('Запрашиваем данные созданного obj и сравниваем их с отправленными'):
            lko_admin.aa_check_alert_data(alert_id, alert_data)
        with allure.step('Проверяем, что в таблицу obj добавилась запись'):
            lko_admin.aa_check_alert_added_to_alerts_table_in_db(alert_id)

    @allure.epic('Int API')
    @allure.feature('Text')
    @allure.story('Получение информации по obj')
    @allure.testcase('https://testrail.dom_name', 'TestCase link on TestRail')
    def test_check_alerts_get_list_request(self, lko_admin):
        with allure.step('Запрос списка obj и проверка ответа'):
            lko_admin.aa_get_alerts_and_check_it()

    @allure.epic('Int API')
    @allure.feature('Text')
    @allure.story('Получение информации об алерте по его id')
    @allure.testcase('https://testrail.dom_name', 'TestCase link on TestRail')
    def test_check_alert_get_info_request(self, lko_admin):
        with allure.step('Выбираем рандомный obj'):
            lko_admin.aa_create_alerts_if_not_enough(1)
            alert_id = lko_admin.aa_get_random_alerts(1)[0]
        with allure.step('Запрашиваем информацию по выбранному obj и проверяем её'):
            lko_admin.aa_get_alert_info_and_check_it(alert_id)

    @allure.epic('Int API')
    @allure.feature('Text')
    @allure.story('Запрос информации о нескольких алертах по списку их id')
    @allure.testcase('https://testrail.dom_name', 'TestCase link on TestRail')
    def test_get_alerts_info_by_ids_list(self, lko_admin):
        with allure.step('Выбираем несколько obj'):
            lko_admin.aa_create_alerts_if_not_enough(3)
            alert_ids = lko_admin.aa_get_random_alerts(3)
        with allure.step('Запрашиваем информацию по выбранным id и проверяем ее'):
            lko_admin.aa_get_alerts_info_by_ids_ad_check_it(alert_ids)

    @allure.epic('Int API')
    @allure.feature('Text')
    @allure.story('Отметка одного obj как ложное срабатывание. Снятие отметки о ложном срабатывании')
    @allure.testcase('https://testrail.dom_name', 'TestCase link on TestRail')
    def test_mark_alert_false_positive_and_back(self, lko_admin):
        with allure.step('Выбираем случайный obj'):
            ids = lko_admin.aa_get_random_alerts(1)
        with allure.step('Отмечаем выбранный obj как ложное срабатывание и проверяем, что метка проставилась'):
            lko_admin.aa_mark_alerts_false_positive_and_check_it(alert_ids=ids)
        with allure.step('Снимает отметку о ложном срабатывании у этого obj и проверяем, что она снялась'):
            lko_admin.aa_unmark_alerts_false_positive_and_check_it(alert_ids=ids)

    @allure.epic('Int API')
    @allure.feature('Text')
    @allure.story('Назначение obj на оператора и снятие назначенного оператора')
    @allure.testcase('https://testrail.dom_name', 'TestCase link on TestRail')
    def test_assign_operator_to_alert(self, lko_admin):
        with allure.step('Выбираем рандомный obj'):
            alert_id = lko_admin.aa_get_random_alerts(1)[0]
        with allure.step('Назначаем obj на оператора'):
            operator_id = lko_admin.sa_get_operator()['id']
            lko_admin.aa_assign_operator_to_alert(alert_id=alert_id, operator_id=operator_id)
        with allure.step('Проверяем, что оператор назначился'):
            lko_admin.aa_check_responsible_operator_id(alert_id, operator_id)
        with allure.step('Меняем назначение на Не назначен'):
            lko_admin.aa_unassign_operator_to_alert(alert_id=alert_id)
        with allure.step('Проверяем, что оператор снялся'):
            lko_admin.aa_check_responsible_operator_absent(alert_id)

# and more more here

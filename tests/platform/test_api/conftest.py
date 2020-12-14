from framework.platform.api_auto.pl_api_workers import IamApiAdmin, OnlyAdmin
import pytest


@pytest.fixture(scope='session')
def iam_admin(stand):
    client = IamApiAdmin(stand)
    return client


@pytest.fixture(scope='session')
def only_admin(iam_admin, stand):
    result = iam_admin.iam_check_if_user_already_exists_in_iam(iam_admin.ONLY_ADMIN_CRED)
    if not result:
        pytest.skip(f'В IAM нет пользователя с логином {iam_admin.ONLY_ADMIN_CRED} с правами только администратора '
                    f'для платформы, тест пропускаем')
    else:
        client = OnlyAdmin(stand)
        return client

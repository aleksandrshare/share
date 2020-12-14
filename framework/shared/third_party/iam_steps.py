from framework.shared.third_party.iam_services import IamCore


class IamActions(IamCore):
    def iam_check_if_user_already_exists_in_iam(self, username):
        resp = self.get_iam_sites()
        site_id = resp[0]['id']
        resp = self.get_iam_site_users(site_id)
        for user in resp["items"]:
            if user["userName"] == username:
                user_id = user["id"]
                self.log.info("Найден пользователь " + username + " с ID " + str(user_id))
                return user_id
        self.log.info("Пользователь " + username + " не найден")
        return None

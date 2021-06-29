from .InitializationException import InitializationException
from .config import BaseConfig, logger, V3, CHOICES
from collections import OrderedDict
from .scheduler import Scheduler
from .router import Router
from .DB import DB

import json


class MailAggregator:
    # region class initialization
    def __init__(self, path, *args, **kwargs):
        self.mails = OrderedDict()
        self.path = path

    # endregion

    def __getitem__(self, value, *args, **kwargs):
        return self.mails.get(value, False)

    # region add new instances
    def __add__(self, value, *args, **kwargs):
        if not isinstance(value, str):
            return
        for class_name in [Scheduler, Router]:
            try:
                instance = class_name(value)
                self._add_instance(instance)
                return
            except InitializationException:
                pass

    def _add_instance(self, instance, *args, **kwargs):
        if isinstance(instance, Scheduler):
            mail = self.mails.get(instance.code, False)
            # print(mail)
            mail and mail + instance
        elif isinstance(instance, Router):
            # print(instance.code)
            if self.mails.get(instance.code, False):
                logger.warning("Code: {}, repeates in logs.".format(instance.code))
            self.mails[instance.code] = instance

    # endregion

    # region string representaion of class
    def __str__(self, n=None, *args, **kwargs):
        return self._get_list_string(n=n)

    def show(
        self, choice=CHOICES[0], n=None, code=list(), mail=list(), *args, **kwargs
    ):
        good_mails, bad_mails, all_mails = self._get_good_and_bad_mails()
        code_and_mails = code + mail

        if choice == "good" and "good" in CHOICES:
            filtered_mails = good_mails
        elif choice == "bad" and "bad" in CHOICES:
            filtered_mails = bad_mails
        else:
            # filtered_mails = list(self.mails.values())
            filtered_mails = sorted(list(self.mails.values()), key=lambda x: x.is_ok)

        filtered_mails = (
            len(code_and_mails)
            and self._filter_by_mail_or_code(filtered_mails, code_and_mails)
            or filtered_mails
        )
        return (
            self._get_list_string(n=n, mails=filtered_mails)
            if len(filtered_mails)
            else "No data matching this query was found."
        )

    def _get_list_string(
        self, n=None, mails=None, message="\tList of mail objects:\n", *args, **kwargs
    ):
        mails = mails or list(self.mails.values())
        length = len(mails)
        n = n and min(n, length) or length
        end = min(n, length)
        payload = "\n{}".format(message)
        for i, mail in enumerate(mails[:end], start=1):
            payload += "{:<4} - {}\n".format(i, mail)
        payload += "\tShow: {}, Overall: {}".format(n, length)
        return payload

    # endregion

    # region filtration data

    def _filter_by_mail_or_code(self, mails, mail_or_code=list(), *args, **kwargs):
        filtered_mails = [x for x in mails if x[mail_or_code]]
        return filtered_mails

    def _get_good_and_bad_mails(self, filtered_list=None, *args, **kwargs):
        filtered_list = filtered_list or list(self.mails.values())
        good_mails, bad_mails = list(), list()
        mails = dict()

        for router in filtered_list:
            for mail in router.mails:
                mails[mail] = router.is_ok or mails.get(mail, router.is_ok)

        for mail in list(mails.keys()):
            if mails[mail]:
                good_mails.append(mail)
            else:
                bad_mails.append(mail)

        return good_mails, bad_mails, list(mails.values())

    # endregion

    # region save data
    def save_to_file(self, *args, **kwargs):
        bad_mails = self._get_good_and_bad_mails(show="bad")
        good_mails = self._get_good_and_bad_mails(show="good")
        with open(BaseConfig.BAD_MAILS, "w") as f:
            f.write(json.dumps(bad_mails))
        with open(BaseConfig.GOOD_MAILS, "w") as f:
            f.write(json.dumps(good_mails))

    def save_sqlite(self, *args, **kwargs):
        db = DB(self.path)
        self._insert_codes(self._get_codes(), db)
        self._insert_mails(self._get_mails(), db)
        db.close()

    def _get_mails(self, *args, **kwargs):
        payload = list()
        for value in list(self.mails.values()):
            payload += value.get_sql_values()
        return payload

    def _insert_mails(self, mails, db, *args, **kwargs):
        query = "INSERT INTO mail(code_id, mail, status_id) VALUES {}".format(
            ",".join(x for x in mails)
        )
        db.execute(query)

    def _get_codes(self, *args, **kwargs):
        codes = list()
        for i, key in enumerate(list(self.mails.keys()), start=1):
            self.mails[key].id = i
            codes.append(key)
        return codes

    def _insert_codes(self, codes, db, *args, **kwargs):
        query = "INSERT INTO code(code) VALUES {}".format(
            ",".join("('{}')".format(x) for x in codes)
        )
        db.execute(query)

    # endregion

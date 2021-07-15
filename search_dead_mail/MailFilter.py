from .Choices import Choices


class MailFilter:
    def __init__(self, mails, code_and_mail, *args, **kwargs):
        self.filtered_mails = self._get_filtered_mails(mails, code_and_mail)
        self._get_sorted_mails()
        self.mails = sorted(mails, key=lambda x: x.is_ok)

    def __getitem__(self, value, *args, **kwargs):
        if isinstance(value, int) or isinstance(value, slice):
            return self.mails[value]
        raise IndexError

    def get(self, value, *args, **kwargs):
        choice = Choices()
        if value is choice.good:
            return self.good_mails
        elif value is choice.bad:
            return self.bad_mails
        return self.sorted_mails

    def __iter__(self, *args, **kwargs):
        self.___iter_index = 0
        return self

    def __next__(self, *args, **kwargs):
        try:
            payload = self[self.___iter_index]
            self.___iter_index += 1
            return payload
        except IndexError:
            raise StopIteration

    def next(self, *args, **kwargs):
        return self.__next__()

    def _get_sorted_mails(self, *args, **kwargs):
        def _sort_function(value, *args, **kwargs):
            if value.is_ok:
                self.good_mails.append(value)
                return True
            self.bad_mails.append(value)
            return False

        self.good_mails = list()
        self.bad_mails = list()

        self.sorted_mails = sorted(self.filtered_mails, key=_sort_function)

    def _get_filtered_mails(self, mails, code_and_mail, *args, **kwargs):
        if code_and_mail is None or not len(code_and_mail):
            return mails

        def _filter(value, *args, **kwargs):
            try:
                value[code_and_mail]
                return True
            except IndexError:
                return False

        filtered_mails = filter(_filter, mails)
        return filtered_mails

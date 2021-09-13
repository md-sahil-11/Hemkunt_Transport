from finance.models import Party, Transaction, TransactionMode


class TransactionBase:
    def __init__(self, data):
        self.value = data["value"]
        self.mode = data["mode"]
        self.party_name_id = data["party"]
        self.comment = data["comment"]
        self.date = data["date"]

    def get_value(self):
        return float(self.value)

    def get_mode_instance(self):
        obj, _ = TransactionMode.objects.get_or_create(name=self.mode.strip().upper())
        return obj

    def get_party_instance(self):
        party_id = self.party_name_id.split("~")[-1]
        return Party.objects.get(id=party_id)

    def create_transaction(self):
        value = self.get_value()
        mode = self.get_mode_instance()
        party = self.get_party_instance()

        comment = self.comment
        date = self.date
        t = Transaction(mode=mode, value=value, date=date, party=party, comment=comment)
        t.save()
        return t

    def create(self):
        return self.create_transaction()


class Payment(TransactionBase):
    def get_value(self):
        return float(self.value) * -1


class Receipt(TransactionBase):
    pass

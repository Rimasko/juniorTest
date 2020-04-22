import csv
import io
from datetime import datetime

from stockmarket.models import Customer, Deal


def load_deals_file_to_db(file):
    """
    парсит csv файл и загружает в БД
    :param file: InMemoryUploadedFile
    :return: статус парсинга
    """
    fieldname = ['customer', 'item', 'total', 'quantity', 'date']
    deals_reader = csv.DictReader(io.StringIO(file.read().decode('utf-8')))
    if len(set(fieldname) ^ set(deals_reader.fieldnames)) > 0:
        return {"Status": "Error",
                "Desc": "проверьте правильность колонок файлв 'customer', 'item', 'total', 'quantity', 'date' "}
    for deal_row in deals_reader:
        customer, _ = Customer.objects.get_or_create(username=deal_row["customer"])
        deal_date = datetime.strptime(deal_row["date"], "%Y-%m-%d %H:%M:%S.%f")
        deal, created = Deal.objects.get_or_create(
            customer=customer,
            item=deal_row["item"],
            total=int(deal_row["total"]),
            quantity=int(deal_row["quantity"]),
            date=deal_date)
        if created:
            customer.spent_money += int(deal_row["total"])
            deal.save()

    data = {"Status": "Ok"}
    return data
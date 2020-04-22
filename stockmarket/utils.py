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

    # удаляем инфомрацию о старых сделках
    Customer.objects.all().delete()

    deals_list = []
    customers_dict = {}
    deals_information = []

    for deal_row in deals_reader:
        name = deal_row["customer"]
        if name not in customers_dict:
            customer = Customer(username=name)
            customers_dict[name] = customer
        # собираем информацию о сделке
        deal_date = datetime.strptime(deal_row["date"], "%Y-%m-%d %H:%M:%S.%f")
        deals_information.append({
            "customer": name,
            "item": deal_row["item"],
            'total': int(deal_row["total"]),
            'quantity': int(deal_row["quantity"]),
            'date': deal_date

        })
    # создаются все покупатели
    Customer.objects.bulk_create(customers_dict.values())

    for deal_row in deals_information:
        customers_dict[deal_row["customer"]].spent_money += int(deal_row["total"])
        deal = Deal(
            customer=customers_dict[deal_row["customer"]],
            item=deal_row["item"],
            total=deal_row["total"],
            quantity=deal_row["quantity"],
            date=deal_row["date"])
        deals_list.append(deal)

    # записываются сделки в базу
    Deal.objects.bulk_create(deals_list)
    # обновление потраченных денег
    Customer.objects.bulk_update(customers_dict.values(), fields=["spent_money"])
    data = {"Status": "Ok"}
    return data

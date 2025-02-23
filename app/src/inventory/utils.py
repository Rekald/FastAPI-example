import os
import pandas as pd
from pathlib import Path

from src.dependencies import tmp_root
from src.inventory.models import InventoryRow


def get_dataframe_from_inventory(inventory: list[InventoryRow]):
    producer_list = []
    total_map = {}
    margin_map = {}
    for row in inventory:
        if row.producer not in producer_list:
            producer_list.append(row.producer)
            total_map[row.producer] = 0
            margin_map[row.producer] = 0
        total_map[row.producer] = total_map[row.producer] + row.total_value
        margin_map[row.producer] = margin_map[row.producer] + ((row.catalog_price * row.quantity) - row.total_value)

    total_list = [total_map[producer] for producer in producer_list]
    margin_list = [margin_map[producer] for producer in producer_list]
    return pd.DataFrame([producer_list, total_list, margin_list], index=['Producer', 'Total', 'Marginality']).T


def gen_xls_report(dataframe):
    dataframe.sort_values(by=['Total'], ascending=False)
    start_row = 1
    Path(tmp_root).mkdir(exist_ok=True)
    report_path = os.path.join(tmp_root, 'Inventory report.xlsx')

    writer = pd.ExcelWriter(report_path, engine='xlsxwriter')
    dataframe.to_excel(writer, sheet_name='Sheet1', startrow=start_row)

    book = writer.book
    sheet = writer.sheets['Sheet1']
    total_chart = book.add_chart({'type': 'pie'})
    total_chart.add_series(
        {
            "name": "Inventory top 5 total value",
            "categories": ["Sheet1", 2, 1, start_row + 5, 1],
            "values": ["Sheet1", 2, 2, start_row + 5, 2],
            'data_labels': {'percentage': True, 'position': 'best_fit'},
        }
    )
    total_chart.set_title({"name": "Inventory top 5 total value"})
    total_chart.set_style(10)
    sheet.insert_chart("G1", total_chart)
    writer.close()
    return report_path


def remove_file(file_path):
    Path(file_path).unlink(missing_ok=True)

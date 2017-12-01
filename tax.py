#!/usr/bin/python
from __future__ import print_function

import csv
import math
from StringIO import StringIO
import argparse

EXCEMPT_STOP_WORDS = ["food", "book", "chocolate", "pills", "medic"]

def round_off(_accfloat, prec=0.05):
    """
     Arguments:
       _accfloat: Number to be rounded off
       prec: Nearest digit to be rounded off

     >>> round_off(4.123)
     4.1
     >>> round_off(4.131)
     4.15
     >>> round_off(4.331)
     4.35
    """
    val = round(_accfloat/prec) * prec
    return float(str(val))

class Item(object):
    """
       Each item has name, price 
       and tax calculation depends
       on whether it is imported or the category to which it belongs.

       >>> item = Item("something", 20, imported=False, excempted=False)
       >>> float(item.tax)
       2.0
       >>> item = Item("something", 20, imported=True, excempted=False)
       >>> float(item.tax)
       3.0
       >>> item = Item("something", 20, imported=True, excempted=False, quantity=2)
       >>> float(item.tax)
       6.0

       >>> item = Item.from_dict({"Product": "imported goods", "Quantity": 2, "Price": 20})
       >>> item.imported
       True
       >>> float(item.tax)
       6.0
       >>> item = Item.from_dict({"Product": "imported food item", "Quantity": 2, "Price": 20})
       >>> item.excempted
       True
       >>> float(item.tax)
       2.0
    """
    def __init__(self, name, price, imported=False, excempted=False, quantity=1):
        self.name = name
        self.price = price
        self.imported = imported
        self.excempted = excempted
        self.quantity = quantity
    
    @property
    def tax(self):
        percentage = 0
        if self.imported:
            percentage += 5
        if not self.excempted:
            percentage += 10
        total_tax = (float(percentage) / 100) *  self.price * self.quantity
        return round_off(total_tax)

    @classmethod
    def from_dict(cls, row):
        name = row["Product"]
        name_lower = name.lower()
        is_excempted = any(map(lambda x: x in name_lower, EXCEMPT_STOP_WORDS))
        is_imported = True if "imported" in name_lower else False
        return cls(name,
                   float(row["Price"]),
                   imported=is_imported,
                   excempted=is_excempted,
                   quantity=int(row["Quantity"]))


class Cart(object):
    
    """
       Cart items
       >>> item1 = Item("Book", 12.49, quantity=1, excempted=True)
       >>> item2 = Item("music cd", 14.99, quantity=1, excempted=False)
       >>> item3 = Item("chocolate bar", 0.85, quantity=1, excempted=True)
       >>> carts = Cart([item1, item2, item3])
       >>> len(carts.items)
       3
    """

    def __init__(self, items):
        self.items = items
    
    def __str__(self):
        total, sales_tax = 0, 0
        buf = StringIO()
        field_names = ["Quantity", "Product", "Price"]
        writer = csv.DictWriter(buf, fieldnames=field_names)
        writer.writeheader()
        for item in self.items:
            total += item.price
            sales_tax += item.tax
            qn = {"Quantity": item.quantity, "Product": item.name, "Price": "{:5.2f}".format(item.price + item.tax)}
            writer.writerow(qn)
            
        csv_value = buf.getvalue() + "\n"
        csv_value += "Sales Tax: {:5.2f}".format(sales_tax) + "\n"
        csv_value += "Total: {:5.2f}".format(total + sales_tax)
        return csv_value

    @classmethod
    def parse_input(cls, input_file):
        reader = csv.DictReader(input_file)
        items = []
        for row in reader:
            items.append(Item.from_dict(row))
        return cls(items)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
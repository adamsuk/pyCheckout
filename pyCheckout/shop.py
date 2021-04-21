"""
shopping - python module for calculating the cost of
a customers cart including discounts.
"""
import os
import sys

# relative imports
from common import read_json
from common import dict_sub_filter

class Shopping:
    def __init__(self,
                 cart_list=[],
                 prices_file="prices/rrp.json",
                 prices_key="items",
                 discounts_file="prices/discounts.json",
                 discount_key="discounts",
                 sort_key="product"
                ):
        # useful to define
        self.basepath = os.path.abspath(os.path.dirname(__file__))
        # define self variables - derived from inputs
        self.cart_list = [cart_item.lower() for cart_item in cart_list]
        self.prices_file = os.path.abspath(os.path.join(self.basepath,
                                                        prices_file))
        self.discounts_file = os.path.abspath(os.path.join(self.basepath,
                                                           discounts_file))
        # define self variables - needed across multiple methods
        self.prices_dict = {}
        self.discounts_dict = {}
        self.cart_dict = {}
        self.cart_savings_dict = {}
        self.cart_subtotal = 0
        self.cart_discount = 0
        self.cart_total = 0
        # call methods needed when instantiated
        if self.prices_file:
            self.prices_dict = read_json(json_file=self.prices_file,
                                         nested_key=prices_key,
                                         sort_key=sort_key)
        # get the cart rrp if a raw list is defined
        if self.cart_list:
            self.cart_rrp()
        # now deal with the discounts
        if self.discounts_file:
            self.discounts_dict = read_json(json_file=self.discounts_file,
                                            nested_key=discount_key,
                                            sort_key=sort_key)
        if self.cart_list:
            self.cart_discounts()

    def cart_rrp(self):
        """
        Method used to determine the RRP total of the current cart
        """
        # get a filtered dictionary of self.prices based on the keys in raw_cart_dict
        raw_cart_dict, self.cart_dict = dict_sub_filter(self.prices_dict, self.cart_list, all_keys_req=True)
        # determine if values in cart_dict are int/floats and multiply by the number of occurances in raw_cart_dict
        for item, props in self.cart_dict.items():
            for prop, val in sorted(props.items()):
                if isinstance(val, (int,float)):
                    self.cart_dict[item][prop] = val * raw_cart_dict[item]
        print(self.cart_dict)

    def cart_discounts(self):
        """
        Method used to determine the discounts to apply to the current cart
        """
        # get a filtered dictionary of self.prices based on the keys in raw_cart_dict
        raw_cart_dict, self.cart_savings_dict = dict_sub_filter(self.discounts_dict, self.cart_list)
        # determine if values in cart_dict are int/floats and multiply by the number of occurances in raw_cart_dict
        for item, props in self.cart_savings_dict.items():
            if "requires" in props.keys():
                # check for product and quantity required from discount dictionary
                if props["requires"]["product"] in self.cart_dict.keys() and \
                        self.cart_dict[props["requires"]["product"]]["quantity"] >= props["requires"]["quantity"]:
                    # determine how many items are discounted
                    print(self.cart_dict[item]["quantity"])
                    print(props["requires"]["quantity"])
                    # quantity based off the number of required items
                    discount_quantity = self.cart_dict[props["requires"]["product"]]["quantity"] // props["requires"]["quantity"]
                    # get min of discount_quantity due to required item threshold and actual item quantity
                    # i.e you can't have more discounts then items you're buying
                    discount_quantity = min(discount_quantity, self.cart_dict[item]["quantity"])
                    requirements_met = True
                else:
                    discount_quantity = 0
                    requirements_met = False
            else:
                discount_quantity = self.cart_dict[item]["quantity"]
                requirements_met = True
            if requirements_met:
                # check for supported discount types
                if props["discount_type"] == "percent":
                    # determine current cost from prices_dict
                    print(item)
                    print(discount_quantity)
                    print(requirements_met)
                    print(self.prices_dict[item])
                    cur_cost = self.prices_dict[item]["price"] * discount_quantity
                    # calculate discount
                    item_discount = (cur_cost / 100) * (props["discount"])
                    self.cart_savings_dict[item]["total_item_discount"] = item_discount
                else:
                    print("Error: discount type of '{}' for '{}' currently unsupported".format(props["discount_type"], item))
            else:
                self.cart_savings_dict[item]["total_item_discount"] = 0
        print(self.cart_savings_dict)

    def __str__(self):
        rtn_str = []
        rtn_str.append("Receipt:\n---------")
        rtn_str.append("Items: Quantity\n---------")
        # cart quantities
        for item, items_props in sorted(self.cart_dict.items()):
            rtn_str.append("{}: {}".format(item, items_props["quantity"]))
        rtn_str.append("---------\nCost:\n---------")
        # cost breakdown
        rtn_str.append("Subtotal: £{:.2f}".format(self.cart_subtotal))
        if self.cart_savings_dict:
            for item_disc, disc_props in sorted(self.cart_savings_dict.items()):
                rtn_str.append("{} {} off: -£{:.2f}".format(item_disc,
                                                            disc_props["discount_type"],
                                                            disc_props["total_item_discount"]))
        else:
            rtn_str.append("(no offers available)")
        rtn_str.append("Total: £{:.2f}".format(self.cart_total))
        return '\n'.join(rtn_str)

if __name__ == "__main__":
    Shopping()

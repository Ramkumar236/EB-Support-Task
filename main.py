import json
import csv


def get_info():
    details = [open('maojson_1.json'), open('maojson_2.json'), open('maojson_5.json'),
               open("auth_mismatch_with_tax.json")]

    for detail in details:
        data = json.load(detail)  # loading all the details from the json files
        order_id = data["OrderId"]
        date = data["CapturedDate"]
        order_status = ""
        tax_shipping = 0
        credit_card = 0
        paypal = 0

        total_amount = data["Payment"][0]["PaymentMethod"][0]["Amount"]
        # print(total_amount)
        payment_method = data["Extended"]["PrimaryPaymentMethod"]
        # print(payment_method)

        gc_rewards_amt = 0
        if payment_method == 'Gift Card':
            gc_rewards_amt = total_amount
        else:
            order_details = data["OrderLine"]
            tax = 0
            for order_line_tax in order_details:
                unit_tax = order_line_tax["OrderLineTaxDetail"]
                for tax_amount in unit_tax:
                    tax = round((tax + tax_amount["TaxAmount"]), 2)

            orders = data["OrderTaxDetail"]
            order_tax_details = 0
            for order in orders:
                order_tax_details = order_tax_details + order["TaxAmount"]

            tax = tax + order_tax_details
            shipping_amounts = data["OrderChargeDetail"]
            final_shipping_amount = 0

            for ChargeTotal in shipping_amounts:
                final_shipping_amount = final_shipping_amount + round(ChargeTotal.get("ChargeTotal"), 2)
            tax_shipping = round((tax + final_shipping_amount), 2)
        unit_price = 0
        for price in data["OrderLine"]:
            unit_price = round((float(unit_price) + float(price["UnitPrice"])), 2)
        tax_shipping_unit = round((round(tax_shipping, 2) + round(unit_price, 2)), 2)

        if total_amount == tax_shipping_unit:
            difference = 0
        else:
            difference = round((total_amount - tax_shipping_unit), 2)
            # print("dd=",difference)

        if data["IsConfirmed"] == True and data["IsOnHold"] == False:
            order_status = 'Placed Successfully'
        elif data["IsConfirmed"] == False and data["IsOnHold"] == True:
            order_status = 'On-Hold'

        payment_count = 0

        pay = data["Payment"]
        for get_pay in pay:
            for pay_type in get_pay["PaymentMethod"]:
                if "Credit Card" in pay_type["PaymentType"].values():
                    payment_count += 1
                    credit_card += 1
                elif "PayPal" in pay_type["PaymentType"].values():
                    payment_count += 1
                    paypal += 1
                elif "Gift Card" in pay_type["PaymentType"].values():
                    payment_count += 1
                elif "Loyalty Certificate" in pay_type["PaymentType"].values():
                    payment_count += 1
        # print(payment_count, end="\n")

        csv_rows = [date, order_id, order_status, unit_price, tax_shipping_unit, total_amount, difference, credit_card,
                    paypal,
                    gc_rewards_amt, payment_count]

        csv_filename = "auth_0208.csv"
        with open(csv_filename, 'a', newline='') as extract_to_csv:
            derived_values = csv.writer(extract_to_csv)
            derived_values.writerow(csv_rows)
            extract_to_csv.close()

        # print(date)
        # print(order_id)
        # print(order_status)
        # print(unit_price)
        # print(tax_shipping_amount)
        # print(total_amount)
        # print(payment_method)


get_info()

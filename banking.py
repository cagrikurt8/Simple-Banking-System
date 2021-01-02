# Write your code here
import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
create_table = '''CREATE TABLE IF NOT EXISTS card(
                             id INTEGER,
                             number TEXT,
                             pin TEXT,
                             balance INTEGER);'''
cur.execute(create_table)
conn.commit()
'''
cur.execute("SELECT*FROM card;")
print("DATABASE")
print(cur.fetchall())
print("********************************************************")
'''
def check_luhn(number):
    check_list = list()
    for i in range(len(number[:15])):
        check_list.append(int(number[i]))
        if i % 2 == 0:
            check_list[i] = check_list[i] * 2
        if check_list[i] > 9:
            check_list[i] = check_list[i] - 9
    total = sum(check_list)
    if total % 10 != 0:
        if int(number[15]) != 10 - (total % 10):
            return False
        else:
            return True
    else:
        if int(number[15]) != 0:
            return False
        else:
            return True

def check_if_exist(number, pin):
    cur.execute("SELECT*FROM card;")
    table_list = cur.fetchall()
    number_list = list()
    pin_list = list()
    for i in range(len(table_list)):
        number_list.append(table_list[i][1])
        pin_list.append(table_list[i][2])
    if number_list.count(number) == 0 or pin_list.count(pin) == 0:
        return False

    else:
        return True

def check_if_number_exist(number):
    cur.execute("SELECT*FROM card;")
    table_list = cur.fetchall()
    number_list = list()
    for i in range(len(table_list)):
        number_list.append(table_list[i][1])
    if number_list.count(number) == 0:
        return False

    else:
        return True

class cardGenerator:
    card_number = None
    pin = None

    def generate_card_number(self):
        self.card_number = "400000"+str(random.randint(100000000, 999999999))
        num = self.card_number
        lst = []
        for i in range(len(num)):
            lst.append(int(num[i]))
            if i % 2 == 0:
                lst[i] = lst[i] * 2
            if lst[i] > 9:
                lst[i] = lst[i] - 9
        total = sum(lst)
        if total % 10 != 0:
            check_sum = 10 - (total % 10)
            self.card_number = int(self.card_number + str(check_sum))
        else:
            self.card_number = int(self.card_number + "0")
        return str(self.card_number)

    def generate_pin(self):
        self.pin = random.randint(1000, 9999)
        return str(self.pin)

choice = None
while choice != 0:

    print("1. Create an account\n2. Log into account\n0. Exit")
    choice = int(input(">"))

    if choice == 1:
        print("\nYour card has been created\nYour card number:")
        new_card = cardGenerator()
        card_number = new_card.generate_card_number()
        card_pin = new_card.generate_pin()
        print(card_number)
        print("Your card PIN:")
        print(card_pin)
        print("\n")
        insertion = f"INSERT INTO card(number,pin,balance) VALUES({card_number}, {str(card_pin)}, 0);"
        cur.execute(insertion)
        conn.commit()

    elif choice == 2:
        print("\nEnter your card number:")
        entered_number = input(">")
        print("Enter your card PIN:")
        entered_pin = input(">")
        if check_if_exist(entered_number, entered_pin) == False:
            print("\nWrong card number or PIN!\n")

        else:
            print("\nYou have successfully logged in!")

            while True:
                print("\n1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
                choice = int(input(">"))

                if choice == 1:
                    cur.execute(f"SELECT balance FROM card WHERE number = {entered_number};")
                    balance = cur.fetchone()[0]
                    print(f"\nBalance: {balance}")

                elif choice == 2:
                    cur.execute(f"SELECT balance FROM card WHERE number = {entered_number};")
                    balance = cur.fetchone()[0]
                    print("Enter income:")
                    entered_income = int(input(">"))
                    print("Income was added!")
                    cur.execute(f"UPDATE card SET balance = {balance + entered_income} WHERE number = {entered_number};")
                    conn.commit()

                elif choice == 3:
                    print("\nTransfer")
                    print("Enter card number:")
                    transfer_number = input(">")
                    if transfer_number == entered_number:
                        print("You can't transfer money to the same account!")
                    elif len(transfer_number) == 16:
                        if check_luhn(transfer_number) == True and check_if_number_exist(transfer_number) == True:
                            print("Enter how much money you want to transfer:")
                            transfer_money = int(input(">"))
                            cur.execute(f"SELECT balance FROM card WHERE number = {entered_number};")
                            balance = cur.fetchone()[0]
                            if balance < transfer_money:
                                print("Not enough money!")
                            else:
                                print("Success!")
                                cur.execute(f"SELECT balance FROM card WHERE number = {transfer_number};")
                                transfer_balance = cur.fetchone()[0]
                                cur.execute(f"UPDATE card SET balance = {transfer_money + transfer_balance} WHERE number = {transfer_number};")
                                conn.commit()
                                cur.execute(f"UPDATE card SET balance = {balance - transfer_money} WHERE number = {entered_number};")
                                conn.commit()
                        elif check_luhn(transfer_number) == True and check_if_number_exist(transfer_number) == False:
                            print("Such a card does not exist.")
                        else:
                            print("Probably you made a mistake in the card number. Please try again!")
                    else:
                        print("Such a card does not exist.")

                elif choice == 4:
                    print("\nThe account has been closed!\n")
                    cur.execute(f"DELETE FROM card WHERE number = {entered_number}")
                    conn.commit()
                    break

                elif choice == 5:
                    print("\nYou have successfully logged out!\n")
                    break
                else:
                    print("\nBye!")
                    break

    elif choice == 0:
        print("\nBye!")

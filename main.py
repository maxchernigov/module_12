import pickle
from datetime import datetime, date


class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = value

class Phone(Field):
    def __init__(self, value: str):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: str):
        if len(value) != 10 or not value.isdigit():
            raise ValueError
        self._value = value

class Birthday(Field):
    def __init__(self, birthday: str):
        self.__birthday = None
        self.birthday = birthday

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, birthday: str):
        if birthday:
            try:
                self.__birthday = datetime.strptime(birthday, "%d.%m.%Y").date()
            except ValueError:
                raise ValueError('Not correct birthday')
        else:
            return 'No BD'

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def add_phone(self, phone_add):
        self.phones.append(Phone(phone_add))

    def remove_phone(self, phone_remove):
        phone_to_remove = None
        for phone in self.phones:
            if phone.value == phone_remove:
                phone_to_remove = phone
                break
        if phone_to_remove:
            self.phones.remove(phone_to_remove)

    def find_phone(self, phone_find):
        for phone in self.phones:
            if phone.value == phone_find:
                return phone

    def edit_phone(self, old_phone, new_phone):
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            phone_to_edit.value = new_phone
        else:
            raise ValueError("Phone not found.")

    def days_to_birthday(self):
        current_today = date.today()
        bday = self.birthday.birthday
        birth = bday.replace(year=current_today.year)
        dif_date = birth - current_today
        if dif_date.days > 0:
            return dif_date.days
        else:
            birth = bday.replace(year=current_today.year + 1)
            dif_date = birth - current_today
            return dif_date.days

    def __repr__(self):
        if self.birthday.birthday:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.birthday}"
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook:
    def __init__(self, file_name):
        self.file_name = file_name
        self.load()

    def add_record(self, record: Record):
        if record.name.value not in self.data:
            self.data[record.name.value] = record
            self.save()
            return record
        else:
            raise ValueError("Record with the same name already exists.")

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            self.save()
        else:
            raise ValueError("Record not found.")

    def save(self):
        with open(self.file_name, 'wb') as f:
            pickle.dump(self.data, f)

    def load(self):
        try:
            with open(self.file_name, 'rb') as f:
                self.data = pickle.load(f)
        except FileNotFoundError:
            self.data = {}

    def find_by_name_or_phone(self, query):
        results = []
        for record in self.data.values():
            if query in record.name.value.lower():
                results.append(record)
            else:
                for phone in record.phones:
                    if query in phone.value:
                        results.append(record)
                        break
        return results

if __name__ == '__main__':
    address_book = AddressBook("address_book.pkl")

    while True:
        print("\n1. Add contact")
        print("2. remove contact")
        print("3. Find for name or phone")
        print("4. show all contacts")
        print("5. Exit")

        choice = input("Choise action: ")

        if choice == "1":
            name = input("Enter name: ")
            birthday = input("Enter your date of birth  (дд.мм.рррр): ")
            record = Record(name, birthday)
            phone_count = int(input("How many numbers do you want to add? "))
            for _ in range(phone_count):
                phone = input("Enter your number: ")
                record.add_phone(phone)
            try:
                address_book.add_record(record)
                print("Contact added!")
            except ValueError as e:
                print(str(e))

        elif choice == "2":
            name = input("Enter the name of the contact you want to delete: ")
            try:
                address_book.delete(name)
                print(f"Contact {name} removed!")
            except ValueError as e:
                print(str(e))

        elif choice == "3":
            query = input("Enter a name or phone number to search: ")
            results = address_book.find_by_name_or_phone(query)
            if results:
                print("\nContacts found::")
                for result in results:
                    print(result)
            else:
                print("Contacts not found:.")

        elif choice == "4":
            for contact in address_book.data.values():
                print(contact)

        elif choice == "5":
            print("Thank you for using your address book!")
            break

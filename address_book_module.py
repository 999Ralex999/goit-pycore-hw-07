from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Please enter a valid name")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone must be 10 digits")
        super().__init__(value)
    
    def validate(self, phone) -> bool:
        return len(phone) == 10 and phone.isdigit()
    
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return True
        raise ValueError(f"Phone {old_phone} not found in contact")
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        birthday = self.birthday.value.strftime('%d.%m.%Y') if self.birthday else "Birthday not set"
        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        return False
    
    def get_upcoming_birthdays(self, days_ahead=7):
        today = datetime.now().date()
        upcoming_birthdays = []
        
        for user in self.data.values():
            if user.birthday:
                b_day = user.birthday.value.replace(year=today.year)

                if b_day < today:
                    b_day = b_day.replace(year=today.year + 1)

                delta = (b_day - today).days
                if 0 <= delta < days_ahead:
                    upcoming_birthdays.append({
                        'name': user.name.value,
                        'congratulation_date': self._get_notification_date(b_day).strftime('%d.%m.%Y')
                    })
        
        return upcoming_birthdays

    def _get_notification_date(self, user_birthday):
        notification_date = user_birthday
        if notification_date.weekday() == 5:
            notification_date += timedelta(days=2)
        elif notification_date.weekday() == 6:
            notification_date += timedelta(days=1)
        return notification_date


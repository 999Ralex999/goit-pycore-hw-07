from address_book_module import AddressBook, Record

address_book = AddressBook()

def main():
    print("Welcome to the assistant bot!")
    commands = {
        "hello": greet,
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": birthdays,
        "delete": delete_contact,
        "close": goodbye,
        "exit": goodbye
    }

    while True:
        user_input = input("Enter a command: ")
        cmd, *args = parse_input(user_input)
        if cmd in commands:
            print(commands[cmd](*args))
            if cmd in ["close", "exit"]:
                break
        else:
            print("Invalid command.", "Available commands:", ", ".join(commands.keys()))

def parse_input(input):
    cmd, *args = input.split()
    return cmd.lower(), *args

def input_error(ValueErrorMessage="Invalid input"):
    def decorator(func):
        def wrapper(*args):
            try:
                return func(*args)
            except ValueError:
                return ValueErrorMessage
            except IndexError:
                return "Not enough arguments provided."
        return wrapper
    return decorator

@input_error("Give me name and phone please.")
def add_contact(*args):
    name, phone = args
    record = address_book.find(name)
    if not record:
        record = Record(name)
        address_book.add_record(record)
    record.add_phone(phone)
    return f"Contact {name} added."

@input_error("Give me name and phones to change.")
def change_contact(*args):
    name, old_phone, new_phone = args
    contact = address_book.find(name)
    if contact:
        contact.edit_phone(old_phone, new_phone)
        return "Contact updated."
    return "Contact not found."

@input_error("Give me name please.")
def show_phone(*args):
    name = args[0]
    contact = address_book.find(name)
    if contact:
        return "; ".join(p.value for p in contact.phones)
    return "Contact not found."

def show_all():
    if not address_book.data:
        return "No contacts found."
    return "\n".join(str(contact) for contact in address_book.values())

@input_error("Give me name and birthday please.")
def add_birthday(*args):
    name, birthday = args
    contact = address_book.find(name)
    if contact:
        contact.add_birthday(birthday)
        return "Birthday added."
    return "Contact not found."

def show_birthday(*args):
    name = args[0]
    contact = address_book.find(name)
    if contact and contact.birthday:
        return contact.birthday.value.strftime("%d.%m.%Y")
    return "Contact not found or birthday not set."

def birthdays():
    upcoming = address_book.get_upcoming_birthdays()
    return "\n".join(f"{c['name']} - {c['congratulation_date']}" for c in upcoming) if upcoming else "No upcoming birthdays."

@input_error("Give me name to delete please.")
def delete_contact(*args):
    name = args[0]
    if address_book.delete(name):
        return f"Contact {name} deleted."
    return f"Contact {name} not found."

def greet():
    return "How can I help you?"

def goodbye():
    return "Goodbye!"

if __name__ == "__main__":
    main()

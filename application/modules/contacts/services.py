from application.modules.contacts.models import Contact


def get_contacts() -> list[Contact]:
    contacts_list = Contact.query.order_by(Contact.last_name, Contact.first_name).all()
    return contacts_list

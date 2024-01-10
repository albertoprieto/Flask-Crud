import requests

base_url = 'http://localhost:5000'


def edit_user(user_id, username, email, address, phone):
    edit_data = {
        'id': user_id,
        'username': username,
        'email': email,
        'address': address,
        'phone': phone
    }

    response = requests.post(f'{base_url}/edit', data=edit_data)

    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error: {response.status_code}, {response.json()}")


user_id_to_edit = 1
new_username = 'NewName'
new_email = 'new_email@example.com'
new_address = 'New Address'
new_phone = '123456789'

#edit_user(user_id=user_id_to_edit, username=new_username, email=new_email, address=new_address, phone=new_phone)


def listusers():
    url = 'http://localhost:5000/records'
    response = requests.get(url)

    if response.status_code == 200:
        users = response.json()
        print(users)
    else:
        print(f"Error: {response.status_code}, {response.json()}")

def add(username='', email='', address='', phone=''):

    url = 'http://localhost:5000/add'
    user_data = {
        'username': username,
        'email': email,
        'address': address,
        'phone': phone
    }

    response = requests.post(url, data=user_data)
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error: {response.status_code}, {response.json()}")

def delete():
    url = 'http://localhost:5000/delete'
    user_id_to_delete = 1  # ID del usuario que deseas eliminar

    response = requests.post(url, data={'id': user_id_to_delete})
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error: {response.status_code}, {response.json()}")

#x = input('Operación: ')

#if x in globals() and callable(globals()[x]):
#    globals()[x]()
#else:
#    print("La función no existe.")

add()
delete()

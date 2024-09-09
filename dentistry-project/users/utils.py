def format_phone(phone_number):
    return (
        f'{phone_number[:2]} ({phone_number[2:5]}) {phone_number[5:8]}-'
        f'{phone_number[8:10]}-{phone_number[10:12]}')

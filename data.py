def get_korean_menu(label):
    try:
        return label_menu_data[label]
    except KeyError:
        return label


def get_label(menu):
    inv_label_menu_data = {v: k for k, v in label_menu_data.items()}
    try:
        return inv_label_menu_data[menu]
    except KeyError:
        return menu


label_menu_data = {
    'meat': '고기',
    'chicken': '치킨',
    'Tteokbokki': '떡볶이',
    'chocolate': '초콜릿'
}

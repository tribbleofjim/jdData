def get_month_from_date(date):
    if date is not None:
        try:
            month = date.split('-')[1]
            if month.startswith('0'):
                month = month[1:]
            m = int(month)
            return m - 1
        except IndexError as e:
            print(e)
            return 0


def array_to_list(target_dict):
    for key, value in target_dict.items():
        value = list(value)
        target_dict[key] = value


def get_sell_count(sell_count):
    try:
        sell_count = sell_count[:-1]
        if sell_count.endswith('万'):
            sell_count = sell_count[:-1] + '0000'
        return int(sell_count)
    except(TypeError, ValueError):
        return -1


if __name__ == '__main__':
    print(get_sell_count(None))

def get_season_from_date(date):
    if date is not None:
        try:
            month = date.split('-')[1]
            if month.startswith('0'):
                month = month[1:]
            m = int(month)
            if 1 <= m <= 3:
                return 0
            elif 4 <= m <= 6:
                return 1
            elif 7 <= m <= 9:
                return 2
            else:
                return 3
        except IndexError as e:
            print(e)
            return 0


def array_to_list(target_dict):
    for key, value in target_dict.items():
        value = list(value)
        target_dict[key] = value

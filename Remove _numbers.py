

def remove_credit_card_number(data):
    if isinstance(data, dict):
        #creat a copy of the dictionary keys to help aviod issues
        for key in list(data.keys()):
            if key ==  'credit-card-number':
                del data[key]

        else:
            
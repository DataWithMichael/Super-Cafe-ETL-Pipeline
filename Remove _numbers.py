

def remove_credit_card_number(data):
    if isinstance(data, dict):
        #creat a copy of the dictionary keys to help aviod issues
        for key in list(data.keys()):
            if key ==  'credit-card-number':
                del data[key]

        else:
             remove_credit_card_number(data[key])
    elif isinstance(data, list):
        # Iterate over the list and call the function for each item
        for item in data:
            remove_credit_card_number(item)
    return data
def validate_product_price(product_price):
    product_price_errors = []
    try:
        float_check = float(product_price)
    except Exception as not_floatable:
        product_price_errors.append(len(product_price_errors))
        product_price_errors[len(product_price_errors) - 1] = 'Invalid Price. Please Enter A Number'
        return product_price_errors
    if ',' in product_price:
        product_price_errors.append(len(product_price_errors))
        product_price_errors[len(product_price_errors) - 1] = 'Invalid Price. Please Replace "," With "."'
    dotpos = 0
    dotcheck = False
    for p in range(0, len(product_price)):
        if product_price[p] == '.' and dotcheck == False:
            dotpos = p
            dotcheck = True
        elif product_price[p] == '.' and dotcheck == True:
            product_price_errors.append(len(product_price_errors))
            product_price_errors[len(product_price_errors) - 1] = 'Invalid Price. Multiple "." Detected'
    if dotpos != 0:
        if len(product_price[dotpos:]) > 3:
            product_price_errors.append(len(product_price_errors))
            product_price_errors[len(product_price_errors) - 1] = 'Invalid Price. More Than Two Digits Following "." Detected'
    if float(product_price) <= 10:
        product_price_errors.append(len(product_price_errors))
        product_price_errors[len(product_price_errors) - 1] = 'Invalid Price. Products Sold At Artmuc Online Have To Be Priced At 10.00€ Or More'
    return product_price_errors



def validate_artist_key(artist_key):
        available_keys = []
        available_keys.append(0)
        available_keys[0] = '1234567890'
        available_keys.append(1)
        available_keys[1] = '0987654321'
        for key in available_keys:
            if key == artist_key:
                return True
        return False

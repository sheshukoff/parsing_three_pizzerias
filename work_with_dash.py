from sort_cities import sorted_brand_and_cities

data_frame = sorted_brand_and_cities()

data = []

for city, brands in data_frame.items():
    dodo, tashir, tomato = brands

    data.append({
        'city': city,
        'dodo': dodo,
        'dodo_value': False,
        'tashir': tashir,
        'tashir_value': False,
        'tomato': tomato,
        'tomato_value': False
    },
    )

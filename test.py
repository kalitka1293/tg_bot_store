data = {'csrfmiddlewaretoken': ['zdpdhLaxaz3cpT7U9LEAPFgna3ct8E6TTKO84USFcfTB4515Hz2D2zVM0Nkud6BL'], 'brand': ['Ballu'], 'country': [''], 'price__gt': [''], 'price__lt': ['1616']}
data.pop('csrfmiddleware')

data_x = data.copy()
data_test = {}
for key, value in data_x.items():
    if not value[0]:
        continue
    data_test.update({key:value[0]})

print(data_test)
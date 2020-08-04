from app.models import Reading

def fix_data(arr : list()):
    aux = list()
    for i in arr:
        aux.append({i.data_reading, i.timestamp})
    return aux
    
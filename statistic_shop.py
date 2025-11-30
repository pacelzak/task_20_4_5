import json 
import functools 

def handle_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            print(f"Ошибка: отсутствует ключ {e} в данных")
            return None
        except ZeroDivisionError:
            print("Ошибка: деление на ноль")
            return 0
        except Exception as e:
            print(f"Неожиданная ошибка в {func.__name__}: {e}")
            return None
    return wrapper

        
def read_json(path):
    with open(path, "r", encoding="utf-8") as file: 
        order = json.load(file) 
    return order  

@handle_errors
def high_info(data, type_high): 
    order_id = 0 
    max_indicator = 0 
    for key, value in data.items(): 
        if value[type_high] > max_indicator: 
            order_id = key 
            max_indicator = value[type_high] 
    return order_id 

@handle_errors
def max_sum_order(data, type_max, sum_field=None): 
    group_order = {} 
    for key, value in data.items():
        group_key = value[type_max]
        if sum_field is None:
            add_value = 1
        else:
            add_value = value[sum_field]
        group_order[group_key] = group_order.get(group_key, 0) + add_value
    max_sum = 0 
    max_id = 0 
    for key, value in group_order.items():  
        if value > max_sum: 
            max_id = key 
            max_sum = value
    return max_id

def avg_order(data):  
    sum_price = 0 
    count_order = 0 
    for value in data.values(): 
        sum_price += value["price"] 
        count_order += 1  
    return sum_price/count_order  

def avg_product(data): 
    total_price = 0
    total_quantity = 0
    for value in data.values(): 
        total_price += value["price"]
        total_quantity += value["quantity"]
    return total_price / total_quantity


if __name__ == "__main__":
    
    path_file = read_json("C:/Users/Pavel/Desktop/orders_july_2023.json") 
    print("Номер самого дорого заказа: {}".format(high_info(path_file, "price")))
    print("Номер заказа с самым большим количеством товаров: {}".format(high_info(path_file, "quantity"))) 
    print("Пользователь с саммым большим количеством заказов: {}".format(max_sum_order(path_file, "user_id"))) 
    print("День с самым большим количеством заказов: {}".format(max_sum_order(path_file, "date"))) 
    print("Пользователь с самой большой суммарной стоимостью заказов: {}".format(max_sum_order(path_file, "user_id", "price"))) 
    print("Средняя стоимость заказа в июле: {:.2f}".format(avg_order(path_file)))  
    print("Средняя стоимость товара в июле: {:.2f}".format(avg_product(path_file)))  

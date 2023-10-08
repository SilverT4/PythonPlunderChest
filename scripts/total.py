import warnings,subprocess
from dataclasses import dataclass
sales_tax = 0.0725 # 7.5%
total = 0.00
subtotal = 0.00
est_tax = 0.00 # this will be calculated by subtracting subtotal from the total cause lazy
@dataclass
class PriceObject:
    name:str = ""
    price:float = 0.00
    quantity:int = 0
items:list[PriceObject] = []
def format_price(price:float):
    funni = str(round(price,2)).split(".")
    if int(funni[1]) == 0:
        return "{0}.00".format(funni[0])
    elif funni[1].endswith("0") and int(funni[1]) != 0:
        return "{0}.{1}0".format(funni[0],funni[1])
    else:
        return str(round(price,2))
def isint(in_:str):
    try:
        int(in_)
        return True
    except ValueError:
        return False
def isfloat(in_:str):
    try:
        float(in_)
        return True
    except ValueError:
        return False
def cls():
    subprocess.call("/c cls",None,"C:/Windows/System32/cmd.exe")
def calculate():
    global subtotal,total,est_tax # if i dont then it'll be a pain in the arse
    st = 0.00
    for item in items:
        st += (item.price * float(item.quantity))
    subtotal = st 
    total = subtotal * (1+sales_tax)
    est_tax = total - subtotal
    cls()
def isBlank(obj:PriceObject):
    return obj.name == '' and obj.price == 0 and obj.quantity == 0
def find_item(name):
    return next((item for item in items if item.name == name),PriceObject()) # 
def add_item(name:str,price:float,quantity:int):
    item = find_item(name)
    if not item.name:
        item.name = name 
    if not item.price: item.price = price
    if item.quantity > 0: item.quantity += quantity
    else: item.quantity = quantity
    if isBlank(find_item(name)): items.append(item)
    calculate()
def prompt_rem_quant(item:PriceObject):
    while True:
        print("Removing item: {0}".format(item.name))
        inp = input("How many do you want to remove? (1-{0} or 'all', press C to cancel): ".format(item.quantity))
        if isint(inp):
            remove_item(item.name,int(inp))
            break
        elif inp.lower() == 'all':
            remove_item(item.name,inp)
            break
        elif inp.lower() == 'c':
            cls()
            break
        else:
            print("Invalid input, please try again.")
def prompt_rem():
    while True:
        if len(items) > 0:
            print("Current item list:")
            for i in range(len(items)):
                item = items[i]
                print("{0}. {1} ({2}x${3}: {4})".format(i+1,item.name,item.quantity,format_price(item.price),format_price(round(item.price*float(item.quantity),2)),))
            inp = input("Select an item, or press C to cancel: ")
            if isint(inp):
                prompt_rem_quant(item)
                break
            elif inp.lower() == "c":
                cls()
                break
        else:
            print("No items in list.")
            input("Press return to continue...")
            cls()
            break
def remove_item(name:str,quantity:str|int):
    item = find_item(name)
    if not isBlank(item):
        if quantity == 'all' or (isint(quantity) and int(quantity) >= item.quantity):
            items.remove(item) # Remove the item.
        else:
            item.quantity -= int(quantity)
        calculate()
    else:
        warnings.warn("Could not find {0} in item list!".format(name),Warning)
        input("Press return to continue...")
    cls()

def prompt_add_quantity(name:str,price:float):
    while True:
        inp = input("Enter item quantity: ")
        if not isint(inp):
            print("Invalid input, please try again.")
        else: break
    add_item(name,price,inp)
def prompt_add_price(name:str):
    while True:
        inp = input("Enter item price: ")
        if not isfloat(inp):
            print("Invalid input, please try again.")
        else:
            break
    prompt_add_quantity(name,float(inp))
def prompt_add_name():
    while True:
        if len(items) > 0:
            print("Current item list:")
            for i in range(len(items)):
                item = items[i]
                print("{0}. {1} ({2}x{3}: {4})".format(i+1,item.name,item.quantity,format_price(item.price),format_price(round(item.price*float(item.quantity),2)),))
            n = input("Choose an option (1-{0}: Existing item corresponding to that number, n/new: new item): ".format(len(items)))
            if isint(n):
                h = int(n)-1 # subtract 1 from n
                if h == 0:
                    h = 1
                if h >= len(items):
                    h = len(items)-1
                item = items[h]
                prompt_add_quantity(item.name,item.price)
                break
            elif n.lower() == "n" or n.lower == "new":
                prompt_add_price(input("Input item name: "))
                break
            else:
                print("Invalid input, please try again.")
        else:
            prompt_add_price(input("Input item name: "))
            break
            
def view_items():
    print("Items ({0} total):".format(len(items)))
    for i in range(len(items)):
        item = items[i]
        print("{0}. {1} ({2}x{3}: {4})".format(i+1,item.name,item.quantity,format_price(item.price),format_price(round(item.price*float(item.quantity),2)),))
    input("Press return to continue...")
    cls()
def reset():
    items.clear() # iirc that's correct
    calculate()

def view_details():
    print("Detailed information:")
    print("---------------------")
    print("Current subtotal: ${0}".format(format_price(subtotal)))
    print("Estimated tax: ${0}".format(format_price(est_tax)))
    print("Current total: ${0}".format(format_price(total)))
    print("Item count: {0}".format(len(items)))
    print("---------------------")
    input("Press return to continue...")
    cls()

while True:
    print("Your current total is ${0}.".format(format_price(total)))
    print("What do you want to do?")
    print("1. Add an item")
    print("2. Remove an item")
    print("3. Reset")
    print("4. View items")
    print("5. View details")
    act = input("Enter an action (1-5, or Q to quit): ")
    cls()
    match act:
        case "1":
            prompt_add_name()
        case "2":
            prompt_rem()
        case "3":
            reset()
        case "4":
            view_items()
        case "5":
            view_details()
        case "q" | "Q":
            quit()
        case _:
            pass # refresh on invalid option lmao
import json
import os
from dashboard.models import Categoria, DetalleVenta, Producto, Region, Venta


with open(os.path.join(os.path.dirname(__file__), './fake_data/categories.json')) as f:
    cats = json.load(f)

with open(os.path.join(os.path.dirname(__file__), './fake_data/products.json')) as f:
    prods = json.load(f)

with open(os.path.join(os.path.dirname(__file__), './fake_data/regions.json')) as f:
    regs = json.load(f)

with open(os.path.join(os.path.dirname(__file__), './fake_data/sells.json')) as f:
    sells = json.load(f)

with open(os.path.join(os.path.dirname(__file__), './fake_data/sell_details.json')) as f:
    details = json.load(f)


def create_regions():
    Region.objects.bulk_create([Region(name=reg) for reg in regs])

def create_categories():
    Categoria.objects.bulk_create([Categoria(name=cat) for cat in cats])

def create_products():
    to_create = []
    for cat, product in prods.items():
        cag = Categoria.objects.get(name=cat) 
        for prod in product:
            nm = prod['nombre']
            prc = prod['precio']
            to_create.append(Producto(
                name=nm,
                category=cag,
                price=prc
            ))
    Producto.objects.bulk_create(to_create)

def create_sells():
    to_create = []
    for sell in sells:
        reg = Region.objects.get(name=sell['region'])
        to_create.append(Venta(
            sell_date=sell['fecha_venta'],
            region=reg,
            sell_state=sell['estado']
        ))
    Venta.objects.bulk_create(to_create)

def create_sell_details():
    to_create = []
    for sellid, items in details.items():

        sid = int(sellid)
        sll = Venta.objects.get(id=sid)

        for item in items:
            prod = Producto.objects.get(name=item['prod'])
            to_create.append(DetalleVenta(
                sell=sll,
                product=prod,
                qty=item['qty'],
                price=item['price']
            ))
    DetalleVenta.objects.bulk_create(to_create)



# create
create_categories()
create_products()
create_regions()
create_sells()
create_sell_details()

# Inicializar el inventario como una lista de diccionarios
inventory = [
    {
        "name": "Pizza Margarita",
        "price": 12000,
        "quantity": 10,
        "code": 1
    },
    {
        "name": "Pasta con Trufa",
        "price": 15000,
        "quantity": 2,
        "code": 2
    },
    {
        "name": "Salmón a la Parrilla",
        "price": 18000,
        "quantity": 5,
        "code": 3
    },
    {
        "name": "Beef Wellington",
        "price": 25000,
        "quantity": 1,
        "code": 4
    },
    {
        "name": "Ensalada César",
        "price": 8000,
        "quantity": 12,
        "code": 5
    }
]

# Función para agregar un producto al inventario
def add_product():
    print("\n=== AGREGAR PRODUCTO AL INVENTARIO ===")
    
    while True:
        name = input("Ingrese el nombre del producto: ")

        product_exists = False # Variable para controlar si el producto ya existe

        for product in inventory:
            if product["name"].lower() == name.lower():
                print(f"❌ Ya existe un producto con el nombre '{name}'")

                product_exists = True
                break
        
        if product_exists:
            retry = input("¿Desea intentar con otro producto? (s/n): ").lower()

            if retry != 's':
                return
            continue
        
        # Ingresar precio y cantidad si el producto no existe
        while True:
            try:
                price = float(input("Ingrese el precio unitario: "))

                if price <= 0:
                    print("❌ El precio debe ser mayor que 0")
                    continue
                break
            except ValueError:
                print("❌ Por favor ingrese un número válido")
        
        while True:
            try:
                quantity = int(input("Ingrese la cantidad disponible: "))

                if quantity < 0:
                    print("❌ La cantidad no puede ser negativa")
                    continue
                break
            except ValueError:
                print("❌ Por favor ingrese un número entero válido")
        
        # Generar nuevo código para el producto
        new_code = max([product["code"] for product in inventory]) + 1 if inventory else 1
        
        # Crear el nuevo producto
        new_product = {
            "name": name,
            "price": price,
            "quantity": quantity,
            "code": new_code
        }
        
        # Agregar el nuevo producto al inventario
        inventory.append(new_product)

        print(f"✅ Producto '{name}' agregado exitosamente con código {new_code}")
        
        # Preguntar si desea agregar otro producto
        add_another = input("¿Desea agregar otro producto? (s/n): ").lower()

        if add_another != 's':
            break

# Función para buscar un producto por nombre
def search_by_name():
    print("\n=== BUSCAR PRODUCTO POR NOMBRE ===")

    name = input("Ingrese el nombre del producto a buscar: ").lower()

    found = False # Variable para controlar si se encontraron productos

    for product in inventory:
        if name in product["name"].lower(): # lower convierte la cadena a minúsculas
            print(f"\nCódigo: {product['code']}")
            print(f"Nombre: {product['name']}")
            print(f"Precio: ${product['price']}")
            print(f"Cantidad: {product['quantity']}")

            found = True

    if not found:
        print(f"❌ No se encontraron productos con el nombre '{name}'")

# Función para buscar un producto por código
def search_by_code():
    print("\n=== BUSCAR PRODUCTO POR CÓDIGO ===")
    
    while True:
        try:
            code = int(input("Ingrese el código del producto a buscar: "))
            break
        except ValueError:
            print("❌ Por favor ingrese un número entero válido")
    
    found = False

    for product in inventory:
        if product["code"] == code:
            print(f"\nCódigo: {product['code']}")
            print(f"Nombre: {product['name']}")
            print(f"Precio: ${product['price']}")
            print(f"Cantidad: {product['quantity']}")

            found = True
            break
    
    if not found:
        print(f"❌ No se encontró ningún producto con el código {code}")

# Función para actualizar la cantidad de un producto
def update_quantity():
    print("\n=== ACTUALIZAR CANTIDAD DE PRODUCTO ===")
    
    while True:
        try:
            code = int(input("Ingrese el código del producto: "))
            break
        except ValueError:
            print("❌ Por favor ingrese un número entero válido")
    
    # Buscar producto
    product_index = -1 # Variable para la posición del producto - -1 indica que no se encontró

    for i, product in enumerate(inventory):
        if product["code"] == code:
            product_index = i
            break
    
    if product_index == -1:
        print(f"❌ No se encontró ningún producto con el código {code}")
        return
    
    # Ingresar nueva cantidad
    while True:
        try:
            new_quantity = int(input(f"Ingrese la nueva cantidad para '{inventory[product_index]['name']}': "))

            if new_quantity < 0:
                print("❌ La cantidad no puede ser negativa")
                continue
            break
        except ValueError:
            print("❌ Por favor ingrese un número entero válido")
    
    # Actualizar cantidad
    inventory[product_index]["quantity"] = new_quantity

    print(f"✅ Cantidad actualizada para '{inventory[product_index]['name']}' a {new_quantity}")

# Función para calcular el valor total del inventario
def calculate_total_value():
    print("\n=== CALCULAR VALOR TOTAL DEL INVENTARIO ===")
    
    total_value = 0

    for product in inventory:
        product_value = product["price"] * product["quantity"]

        total_value += product_value

        print(f"{product['name']}: ${product_value}")
    
    print(f"\n💵 VALOR TOTAL DEL INVENTARIO: ${total_value}")

# Función para mostrar el inventario
def display_inventory():
    print("\n=== INVENTARIO COMPLETO ===")
    
    if not inventory:
        print("El inventario está vacío")
        return
    
    print(f"{'CÓDIGO':<10}{'NOMBRE':<30}{'PRECIO':<15}{'CANTIDAD':<15}")
    print("-" * 70)
    
    for product in inventory:
        print(f"{product['code']:<10}{product['name']:<30}${product['price']:<14}{product['quantity']:<15}")

# Función para mostrar el menu
def display_menu():
    print("\n===== SISTEMA DE GESTIÓN DE INVENTARIO =====")
    print("1. Agregar producto")
    print("2. Buscar producto por nombre")
    print("3. Buscar producto por código")
    print("4. Actualizar cantidad de producto")
    print("5. Calcular valor total del inventario")
    print("6. Mostrar inventario completo")
    print("7. Salir")
    print("===========================================")

# Función principal
def main():
    while True:
        display_menu()
        
        option = input("\nSeleccione una opción (1-7): ")
        
        if option == "1":
            add_product()
        elif option == "2":
            search_by_name()
        elif option == "3":
            search_by_code()
        elif option == "4":
            update_quantity()
        elif option == "5":
            calculate_total_value()
        elif option == "6":
            display_inventory()
        elif option == "7":
            print("\n¡Gracias por usar el Sistema de Gestión de Inventario!")
            break
        else:
            print("❌ Opción inválida. Por favor, seleccione una opción del 1 al 7.")

if __name__ == "__main__":
    main()
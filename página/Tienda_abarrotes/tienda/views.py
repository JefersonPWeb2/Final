from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Pedido, ItemPedido

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/lista_productos.html', {'productos': productos})

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    return render(request, 'tienda/detalle_producto.html', {'producto': producto})

def carrito_compras(request):
    carrito = request.session.get('carrito', [])  # Obtener el carrito de la sesión
    total = 0
    for item in carrito:
        producto = get_object_or_404(Producto, pk=item['producto_id'])
        item['producto'] = producto
        item['subtotal'] = producto.precio * item['cantidad']
        total += item['subtotal']
    if request.method == 'POST':
        producto_id = int(request.POST.get('producto_id'))
        cantidad = int(request.POST.get('cantidad', 1))
        carrito.append({'producto_id': producto_id, 'cantidad': cantidad})
        request.session['carrito'] = carrito
    return render(request, 'tienda/carrito_compras.html', {'carrito': carrito, 'total': total})

def procesar_pedido(request):
    carrito = request.session.get('carrito', [])

    if request.method == 'POST':
        total = 0
        pedido = Pedido(total=0)  # Crea un objeto de Pedido

        for item in carrito:
            producto = get_object_or_404(Producto, pk=item['producto_id'])
            subtotal = producto.precio * item['cantidad']
            total += subtotal
            # Crea un objeto de ItemPedido relacionado con el Pedido y el Producto
            item_pedido = ItemPedido(producto=producto, cantidad=item['cantidad'], subtotal=subtotal)
            pedido.itempedido_set.add(item_pedido)

        pedido.total = total
        pedido.save()
        request.session['carrito'] = []

        return redirect('tienda:lista_productos.html')  # Redirige a la lista de productos

    return render(request, 'tienda/procesar_pedido.html')
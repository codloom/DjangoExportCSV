# Django Export To CSV

Nesse tutorial vamos exportar os dados de uma tabela para CSV.

Documentação: [https://docs.python.org/3/library/csv.html](https://docs.python.org/3/library/csv.html)

***myapp/views.py***

```python
import csv
import datetime
from django.http import HttpResponse

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Products' + \
        str(datetime.datetime.now())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['Title1','Title2','Title3','Title4']) # head Titulo
    
    products = Product.objects.all() # lista todos os produtos
 
    for product in products:
        image_product = [el.image.url for el in product.products.all()] # todas as imagens do produto
        writer.writerow([product.name, product.price, 
            product.description,image_product])
    return response
```

***myapp/templates/urls.py***

```python
from django.urls import path 
from myapp import views

urlpatterns = [
    path('', views.product_list, name='product-list'), 
    path('create-product/', views.form_product, name='product-create'),
    path('export-csv/', views.export_csv, name='export-csv'),  
]
```

***myapp/templates/index.html***

```python
<a class="btn btn-success" href="{% url 'export-csv' %}">ExportCSV</a>
```

## Django ExportCSV com Filtro

```python
import csv
import datetime
from django.http import HttpResponse

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Products' + \
        str(datetime.datetime.now())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['Title1','Title2','Title3','Title4']) # head Titulo
    
    # products = Product.objects.all() # lista todos os produtos
		obj = request.GET.get('obj')
    # products = Product.objects.filter(name__icontains=obj) # lista todos os produtos 
    print(obj) 
    if obj:  
        products = Product.objects.filter(name__icontains=obj)  
    else:
        products = Product.objects.all()

    for product in products:
        image_product = [el.image.url for el in product.products.all()] # todas as imagens do produto
        writer.writerow([product.name, product.price, 
            product.description,image_product])
    return response
```

```python
<a class="btn btn-success" href="{% url 'export-csv' %}?obj={{request.GET.obj}}">ExportCSV</a>
```
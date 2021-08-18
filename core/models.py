import enum

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    deletion_date = models.DateTimeField(null=True)
    show_in_pos = models.BooleanField()
    show_in_menu_configuration = models.BooleanField()
    parent = models.ForeignKey("Category", on_delete=models.PROTECT, related_name='category_children')


class MajorGroup(models.Model):
    name = models.CharField(max_length=100)
    deletion_date = models.DateTimeField(null=True)


class Family(models.Model):
    name = models.CharField(max_length=100)
    deletion_date = models.DateTimeField(null=True)
    show_in_pos = models.BooleanField()
    show_in_menu_configuration = models.BooleanField()
    major_group = models.ForeignKey(MajorGroup, on_delete=models.PROTECT, related_name='families')
    parent = models.ForeignKey("Family", on_delete=models.PROTECT, related_name='category_families')


class Allergen(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField()


class SalesTax(models.Model):
    name = models.CharField(max_length=100)
    tax = models.FloatField()


class PreparationType(models.Model):
    name = models.CharField(max_length=100)


class PreparationOrder(models.Model):
    name = models.CharField(max_length=100)
    priority = models.IntegerField()
    needsPrinting = models.BooleanField()


class Product(models.Model):
    name = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category)
    family = models.ForeignKey(Family, on_delete=models.PROTECT, null=True)
    is_sold_as_principal_product = models.BooleanField()
    is_sold_as_added = models.BooleanField()
    is_sold_by_weight = models.BooleanField()
    preparation_type = models.ForeignKey(PreparationType, on_delete=models.PROTECT, null=True)
    preparation_order = models.ForeignKey(PreparationOrder, on_delete=models.PROTECT, null=True)
    code_PLU = models.CharField(max_length=100)
    sales_tax = models.ManyToManyField(SalesTax)
    allergens = models.ManyToManyField(Allergen)


class PriceList(models.Model):
    name = models.CharField(max_length=100)
    deletion_date = models.DateTimeField(null=True)


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices')
    price_list = models.ForeignKey(PriceList, on_delete=models.CASCADE, related_name='product_prices')
    main = models.FloatField(null=False)
    added = models.FloatField(null=False)


class Company(models.Model):
    business_name = models.CharField(max_length=100)
    fiscal_name = models.CharField(max_length=100)
    cif = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    web = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    deletion_date = models.DateTimeField(null=True)


class Customer(models.Model):
    business_name = models.CharField(max_length=100)
    fiscal_name = models.CharField(max_length=100)
    cif = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    deletion_date = models.DateTimeField(null=True)


class Supplier(Company):
    apply_equivalence_charge = models.BooleanField()


class Building(models.Model):
    name = models.CharField(max_length=100)


class SaleCenter(models.Model):
    name = models.CharField(max_length=100)
    building = models.ForeignKey(Building, on_delete=models.PROTECT, null=True)


class SaleLocation(models.Model):
    name = models.CharField(max_length=100)
    seats = models.IntegerField()
    sale_center = models.ForeignKey(SaleCenter, on_delete=models.PROTECT, related_name='sale_locations')


class Coin(models.Model):
    name = models.CharField(max_length=100)
    value = models.FloatField()


class Ticket(models.Model):
    sale_location = models.ForeignKey(SaleLocation, on_delete=models.PROTECT, related_name='tickets')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, null=True)
    customer_business_name = models.CharField(max_length=100)
    customer_fiscal_name = models.CharField(max_length=100)
    customer_cif = models.CharField(max_length=100)
    customer_telephone = models.CharField(max_length=100)
    customer_email = models.CharField(max_length=100)
    customer_contact = models.CharField(max_length=100)
    customer_street = models.CharField(max_length=100)
    customer_city = models.CharField(max_length=100)
    customer_region = models.CharField(max_length=100)
    customer_zip_code = models.CharField(max_length=100)

    creation_date = models.DateTimeField(auto_now_add=True)

    discount_rate = models.FloatField()
    discount_total = models.FloatField()
    cash_discount = models.FloatField()

    gross = models.FloatField()
    net = models.FloatField()
    tax = models.FloatField()
    total = models.FloatField()


class SalesTaxLine(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.PROTECT, related_name='tax_lines')
    sales_tax = models.ForeignKey(SalesTax, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    tax = models.FloatField()
    gross = models.FloatField()


class TicketLineStatus(enum.Enum):
    CREATED = 'CREATED'


class TicketLine(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.PROTECT, related_name='lines')
    total_amount = models.FloatField()
    unit_price = models.FloatField()
    discount_rate = models.FloatField()
    discount_total = models.FloatField()
    status = models.CharField(max_length=20, choices=[(x.value, x.name) for x in TicketLineStatus])

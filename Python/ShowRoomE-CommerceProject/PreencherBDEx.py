from datetime import datetime
from ConexãoBDEx import DBConnectionHandler
from ModelosEx import DeliveryType, Order, PaymentType, Payment, Product, User

def create_payment_type():
    with DBConnectionHandler() as db:
        new_payment_type = PaymentType(
            name="Card",
            description="Payment",
            type="Credit Card"
        )

        db.session.add(new_payment_type)
        db.session.commit()
        db.session.refresh(new_payment_type)
        return new_payment_type.pk_payment_type

def create_payment():
    with DBConnectionHandler() as db:
        new_payment = Payment(
            city="Brasília",
            address="SQS 205",
            neighborhood="Plano Piloto",
            country="Brazil",
            value=1000,
            card_name="Test Fidalgo",
            card_number="123456789",
            data_expiration=datetime.now(),
            fk_payment_type=1
        )

        db.session.add(new_payment)
        db.session.commit()
        db.session.refresh(new_payment)
        return new_payment.pk_payment

def create_delivery():
    with DBConnectionHandler() as db:
        new_delivery_type = DeliveryType(
            name="Ifood",
            description="Delivery on your street."
        )

        db.session.add(new_delivery_type)
        db.session.commit()
        db.session.refresh(new_delivery_type)
        return new_delivery_type.pk_delivery

def create_user():
    with DBConnectionHandler() as db:
        new_user = User(
            name = "Testing",
            password = "user123",
            email = "test@user.com",
            cep = "7105098",
            city = "Brasília",
            address = "SQS 21065 Bloco K",
            neighborhood = "Plano Piloto",
            cellphone = "61 9 99999999",
        )

        db.session.add(new_user)
        db.session.commit()
        db.session.refresh(new_user)
        return new_user.pk_user

def create_order(user: int, payment:int, delivery_type:int):
    with DBConnectionHandler() as db:
        new_order = Order(
            fk_user=user,
            fk_payment=payment,
            fk_delivery_type=delivery_type,
            order_number = 1
        )

        db.session.add(new_order)
        db.session.commit()
        db.session.refresh(new_order)
        return new_order.pk_order

def create_order_product(order:str, product:int, quantity:int, total_value:float):
    with DBConnectionHandler() as db:
        query = """
            INSERT INTO Tb_order_product (fk_order, fk_product, quantity, total_value)
            VALUES (:order, :product, :quantity, :total_value)
        """
        db.session.execute(
            query,
            {"order": order, "product": product, "quantity": quantity, "total_value": total_value},
        )
        db.session.commit()

def create_product():
    with DBConnectionHandler() as db:
        new_product = Product(
            name="test",
            description="test product",
            value=123,
            stock=999,
            product_profile_file='ncuey29fn8coau30icna0cnwa'
        )

        db.session.add(new_product)
        db.session.commit()
        db.session.refresh(new_product)
        return new_product.pk_product

if __name__ == '__main__':
    user = create_user()
    result = create_payment_type()
    payment = create_payment()
    delivery_type = create_delivery()
    order = create_order(user=user, payment=payment, delivery_type=delivery_type)
    product = create_product()
    # order_product = create_order_product(order=order, product=product, quantity=1, total_value=1000)
    print(result)
from app.extensions import mongo


def listProducts_resolver(obj, info):
    try:
        products = mongo.db.products.find(projection={
                                          "_id": False, "uuid": True, "name": True, "text": True, "rate_template": True})

        payload = {
            "success": True,
            "products": products
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload



def resolver_test(obj, info, val):
    try:
        payload = {
            "success": True,
            "value": val if val > 10 else 10
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

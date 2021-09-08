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

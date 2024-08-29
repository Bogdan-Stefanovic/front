from sanic import Sanic, response
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
from fuzzywuzzy import process  # Import process for fuzzy matching

app = Sanic("action_server")

products = [
              {
                            "id": 1,
                            "name": 'Cotton T-shirt',
                            "description": 'Comfortable cotton t-shirt',
                            "type": 'Casual',
                            "size": 'M',
                            "manufacturer": 'Brand A',
                            "productionDate": "2023-01-01",
                            "price": 19.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/564x/42/cf/5a/42cf5ad45d3e1c061e6d86f7336c5a63.jpg'
                        },
                        {
                            "id": 2,
                            "name": 'Black T-shirt',
                            "description": 'Comfortable cotton t-shirt in black',
                            "type": 'Casual',
                            "size": 'L',
                            "manufacturer": 'Brand A',
                            "productionDate": "2023-01-01",
                            "price": 21.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/564x/d7/ab/de/d7abde31b08d7df15b1bb8e128a5697a.jpg'
                        },
                        {
                            "id": 3,
                            "name": 'Stylish blue Jeans',
                            "description": 'Stylish blue jeans',
                            "type": 'Casual',
                            "size": 'L',
                            "manufacturer": 'Brand B',
                            "productionDate": "2023-01-01",
                            "price": 49.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/564x/6f/c0/41/6fc041869320f5788bf2567eccd26d42.jpg'
                        },
                        {
                            "id": 4,
                            "name": 'Slim fit Jeans',
                            "description": 'Slim fit jeans',
                            "type": 'Casual',
                            "size": 'M',
                            "manufacturer": 'Brand B',
                            "productionDate": "2023-01-01",
                            "price": 55.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/564x/bb/3d/a1/bb3da1fdd74be6f5768239d540562816.jpg'
                        },
                        {
                            "id": 5,
                            "name": 'Winter Jacket',
                            "description": 'Durable winter jacket',
                            "type": 'Outerwear',
                            "size": 'L',
                            "manufacturer": 'Brand C',
                            "productionDate": "2023-01-01",
                            "price": 89.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/564x/12/2a/01/122a01af3961b972d8ac900c06016331.jpg'
                        },
                        {
                            "id": 6,
                            "name": 'Summer Jacket',
                            "description": 'Lightweight summer jacket',
                            "type": 'Outerwear',
                            "size": 'M',
                            "manufacturer": 'Brand C',
                            "productionDate": "2023-01-01",
                            "price": 79.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/564x/00/09/98/0009981d72b2287af6987e2d1830f69a.jpg'
                        },
                        {
                            "id": 7,
                            "name": 'Running Sneakers',
                            "description": 'Quality running sneakers',
                            "type": 'Footwear',
                            "size": '8',
                            "manufacturer": 'Brand D',
                            "productionDate": "2023-01-01",
                            "price": 59.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/564x/24/d2/4d/24d24d34b24161598e108846dfe2ad56.jpg'
                        },
                        {
                            "id": 8,
                            "name": 'Casual Sneakers',
                            "description": 'Casual sneakers',
                            "type": 'Footwear',
                            "size": '9',
                            "manufacturer": 'Brand D',
                            "productionDate": "2023-01-01",
                            "price": 65.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/564x/53/dd/2d/53dd2d5d755c2152f279121a58192657.jpg'
                        },
                        {
                            "id": 9,
                            "name": 'Evening Dress',
                            "description": 'Elegant evening dress',
                            "type": 'Formal',
                            "size": 'M',
                            "manufacturer": 'Brand E',
                            "productionDate": "2023-01-01",
                            "price": 99.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/564x/13/d1/87/13d18728ea0ef62f9ac65da8e001c00e.jpg'
                        },
                        {
                            "id": 10,
                            "name": 'Summer Dress',
                            "description": 'Casual summer dress',
                            "type": 'Formal',
                            "size": 'S',
                            "manufacturer": 'Brand E',
                            "productionDate": "2023-01-01",
                            "price": 79.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/564x/98/ad/1e/98ad1e225dcd906bb6d10909e124a796.jpg'
                        },
                        {
                            "id": 11,
                            "name": 'Stylish Cap',
                            "description": 'Elegant and stylish hat.',
                            "type": 'Accessories',
                            "size": 'One Size',
                            "manufacturer": 'Brand C',
                            "productionDate": "2023-01-01",
                            "price": 24.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/564x/c7/62/2e/c7622ed3f415431065f6deedf63040f6.jpg'
                        },
                        {
                            "id": 12,
                            "name": 'Baseball Cap',
                            "description": 'Baseball cap',
                            "type": 'Accessories',
                            "size": 'One Size',
                            "manufacturer": 'Brand F',
                            "productionDate": "2023-01-01",
                            "price": 19.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/564x/89/35/fa/8935fa7e830971d983652cf2a5f23faf.jpg'
                        },
                        {
                            "id": 13,
                            "name": 'Wool Scarf',
                            "description": 'Warm wool scarf',
                            "type": 'Accessories',
                            "size": 'One Size',
                            "manufacturer": 'Brand F',
                            "productionDate": "2023-01-01",
                            "price": 29.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/564x/ac/01/51/ac0151cc41c379751acc0afa1c8d140e.jpg'
                        },
                        {
                            "id": 14,
                            "name": 'Summer Scarf',
                            "description": 'Lightweight summer scarf',
                            "type": 'Accessories',
                            "size": 'One Size',
                            "manufacturer": 'Brand F',
                            "productionDate": "2023-01-01",
                            "price": 19.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/564x/9e/13/f6/9e13f6a90457ca77b1933ea3944c41a4.jpg'
                        },
                        {
                            "id": 15,
                            "name": 'Sunglasses',
                            "description": 'Stylish sunglasses',
                            "type": 'Accessories',
                            "size": 'One Size',
                            "manufacturer": 'Brand G',
                            "productionDate": "2023-01-01",
                            "price": 49.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/564x/bb/24/3f/bb243f50e3fa61538bac407885a9421c.jpg'
                        },
                        {
                            "id": 16,
                            "name": 'Watch',
                            "description": 'Elegant wrist watch',
                            "type": 'Accessories',
                            "size": 'One Size',
                            "manufacturer": 'Brand H',
                            "productionDate": "2023-01-01",
                            "price": 199.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/564x/44/f9/72/44f9721cbda958df0bfc823a595e12df.jpg'
                        },
                        {
                            "id": 17,
                            "name": 'Backpack',
                            "description": 'Durable backpack',
                            "type": 'Accessories',
                            "size": 'One Size',
                            "manufacturer": 'Brand I',
                            "productionDate": "2023-01-01",
                            "price": 79.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/564x/7a/4e/4b/7a4e4bc2ed991e4cc6c1330e2e4f9a8b.jpg'
                        },
                        {
                            "id": 18,
                            "name": 'Hat',
                            "description": 'Stylish summer hat',
                            "type": 'Accessories',
                            "size": 'One Size',
                            "manufacturer": 'Brand J',
                            "productionDate": "2023-01-01",
                            "price": 34.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/736x/15/eb/30/15eb309e8bbe27c3c3f458f47d6d1a25.jpg'
                        },
                        {
                            "id": 19,
                            "name": 'Belt',
                            "description": 'Leather belt',
                            "type": 'Accessories',
                            "size": 'L',
                            "manufacturer": 'Brand K',
                            "productionDate": "2023-01-01",
                            "price": 39.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/564x/cd/59/17/cd5917dc6a6fb5dd7df1e76dd5d73bbf.jpg'
                        },
                        {
                            "id": 20,
                            "name": 'Gloves',
                            "description": 'Warm winter gloves',
                            "type": 'Accessories',
                            "size": 'M',
                            "manufacturer": 'Brand L',
                            "productionDate": "2023-01-01",
                            "price": 14.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/564x/9f/22/54/9f225471b5865306a8d16cecdf3f2657.jpg'
                        },
                        {
                            "id": 21,
                            "name": 'Running Sneakers',
                            "description": 'Comfortable running shoes for daily wear',
                            "type": 'Footwear',
                            "size": 'L',
                            "manufacturer": 'Brand C',
                            "productionDate": "2023-01-01",
                            "price": 49.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/564x/17/ed/84/17ed84133aa50a2a16317e89a68e643f.jpg'
                        },
                        {
                            "id": 22,
                            "name": 'Gym T-Shirt',
                            "description": 'Stylish casual shirt for everyday use',
                            "type": 'Casual',
                            "size": 'M',
                            "manufacturer": 'Brand A',
                            "productionDate": "2023-01-01",
                            "price": 24.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/564x/cc/cf/11/cccf11391d8ef5d5ca4186d3a606f2a9.jpg'
                        },
                        {
                            "id": 23,
                            "name": 'Leather Jacket',
                            "description": 'Durable and stylish leather jacket',
                            "type": 'Outerwear',
                            "size": 'XL',
                            "manufacturer": 'Brand B',
                            "productionDate": "2023-01-01",
                            "price": 99.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/564x/31/a8/2a/31a82a3c0f2ae03053ae200462fe82bf.jpg'
                        },
                        {
                            "id": 24,
                            "name": 'Formal Shoes',
                            "description": 'Elegant formal shoes for business occasions',
                            "type": 'Footwear',
                            "size": 'M',
                            "manufacturer": 'Brand E',
                            "productionDate": "2023-01-01",
                            "price": 79.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/736x/cb/3a/8d/cb3a8dd97cc301e3d9b1fdbf9d1091e2.jpg'
                        },
                        {
                            "id": 25,
                            "name": 'Green Dress',
                            "description": 'Lightweight summer dress for casual outings',
                            "type": 'Formal',
                            "size": 'S',
                            "manufacturer": 'Brand F',
                            "productionDate": "2023-01-01",
                            "price": 34.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/564x/62/58/cc/6258cc29d539d3c22ffb90aec89394c2.jpg'
                        },
                        {
                            "id": 26,
                            "name": 'Trendy Sneakers',
                            "description": 'Trendy sneakers for everyday wear',
                            "type": 'Footwear',
                            "size": 'M',
                            "manufacturer": 'Brand D',
                            "productionDate": "2023-01-01",
                            "price": 39.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/564x/32/a9/02/32a90221be0521fcf002296260956882.jpg'
                        },
                        {
                            "id": 27,
                            "name": 'Polo T-Shirt',
                            "description": 'Classic polo shirt for casual and semi-formal wear',
                            "type": 'Casual',
                            "size": 'L',
                            "manufacturer": 'Brand A',
                            "productionDate": "2023-01-01",
                            "price": 29.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/564x/c9/24/52/c92452f990eb7f053baff6f360b4e6ef.jpg'
                        },
                        {
                            "id": 28,
                            "name": 'Denim Jeans',
                            "description": 'Stylish denim jeans for everyday wear',
                            "type": 'Casual',
                            "size": 'M',
                            "manufacturer": 'Brand B',
                            "productionDate": "2023-01-01",
                            "price": 59.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/564x/26/da/68/26da68d20f16eae3397551d7bce5683a.jpg'
                        },
                        {
                            "id": 29,
                            "name": 'Hiking Boots',
                            "description": 'Durable hiking boots for outdoor adventures',
                            "type": 'Footwear',
                            "size": 'XL',
                            "manufacturer": 'Brand C',
                            "productionDate": "2023-01-01",
                            "price": 89.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/564x/c2/94/12/c29412e984db1ad4b574ee401ba58153.jpg'
                        },
                        {
                            "id": 30,
                            "name": 'Beanie Hat',
                            "description": 'Warm beanie hat for cold weather',
                            "type": 'Accessories',
                            "size": 'One Size',
                            "manufacturer": 'Brand D',
                            "productionDate": "2023-01-01",
                            "price": 14.99,
                            "reviews": [],
                            "imageUrl": 'https://i.pinimg.com/564x/dd/67/a1/dd67a16b1a4b22ce939c78451ed6837e.jpg'
                        }
              ]
# Action to get product info
class ActionGetProductInfo(Action):
    def name(self) -> str:
        return "action_get_product_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        product_name = tracker.get_slot("product").lower()

        # Find exact matches
        matched_items = [item for item in products if product_name == item['name'].lower()]

        if matched_items:
            item = matched_items[0]  # Return the exact match
            product_link = f"http://localhost:4200/clothing/{item['id']}"
            response_text = (
                f"Here are the details for '{item['name']}':\n"
                f"Description: {item['description']}\n"
                f"Type: {item['type']}\n"
                f"Size: {item['size']}\n"
                f"Manufacturer: {item['manufacturer']}\n"
                f"Production Date: {item['productionDate']}\n"
                f"Price: ${item['price']:.2f}\n"
            )

            dispatcher.utter_message(text=response_text)
            dispatcher.utter_message(image=item['imageUrl'])
            dispatcher.utter_message(text=product_link)  # Send the product link as a separate message
            return []

        # Find items by category if the exact match is not found
        matched_category_items = [item for item in products if product_name in item['name'].lower() or product_name in item['type'].lower()]

        if matched_category_items:
            for item in matched_category_items:
                product_link = f"http://localhost:4200/clothing/{item['id']}"
                dispatcher.utter_message(image=item['imageUrl'])

                # Include the name, description, and product link after the image
                item_details = (
                    f"{item['name']} (${item['price']:.2f})\n"
                    f"Description: {item['description']}\n"
                    f"{product_link}\n"
                )
                dispatcher.utter_message(text=item_details)

            return []

        # If no match is found, apologize
        dispatcher.utter_message(text=f"Sorry, we don't have information about {product_name}.")
        return []





class ActionGetProductByPrice(Action):
    def name(self) -> str:
        return "action_get_product_by_price"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        min_price = tracker.get_slot("min_price")
        max_price = tracker.get_slot("max_price")

        # Clean up the price values, stripping any dollar signs and whitespace
        if min_price:
            min_price = float(min_price.replace('$', '').strip())
        if max_price:
            max_price = float(max_price.replace('$', '').strip())

        filtered_items = [item for item in products if
                          (min_price is None or item['price'] >= min_price) and
                          (max_price is None or item['price'] <= max_price)]

        if filtered_items:
            for item in filtered_items:
                product_link = f"http://localhost:4200/clothing/{item['id']}"

                # First, display the name and price
                item_details = f"{item['name']} (${item['price']:.2f})"
                dispatcher.utter_message(text=item_details)

                # Then, display the image
                dispatcher.utter_message(image=item['imageUrl'])

                # Finally, display the link
                dispatcher.utter_message(text=product_link)

            # After all individual product details, you can also provide a summary or additional information if needed
        else:
            dispatcher.utter_message(text="Sorry, no products found within the specified price range.")

        return []









# Action to confirm order
class ActionOrderConfirmation(Action):
    def name(self) -> str:
        return "action_order_confirmation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        product_name = tracker.get_slot("product").lower()

        matched_items = [item for item in products if product_name == item['name'].lower()]

        if matched_items:
            item = matched_items[0]  # Find the exact product
            response = f"You have successfully ordered {item['name']}. Your order will be processed shortly."

            # Using metadata instead of a custom event
            dispatcher.utter_message(text=response, metadata={"action": "add_to_cart", "item": item})
            return []

        dispatcher.utter_message(text=f"Sorry, we don't have information about {product_name}.")
        return []




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5055)
#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         product_name = tracker.get_slot("product").lower()
#         clothing_items = [
#               {
#                             "id": 1,
#                             "name": 'T-shirt',
#                             "description": 'Comfortable cotton t-shirt',
#                             "type": 'Casual',
#                             "size": 'M',
#                             "manufacturer": 'Brand A',
#                             "productionDate": "2023-01-01",
#                             "price": 19.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/564x/42/cf/5a/42cf5ad45d3e1c061e6d86f7336c5a63.jpg'
#                         },
#                         {
#                             "id": 2,
#                             "name": 'T-shirt',
#                             "description": 'Comfortable cotton t-shirt in black',
#                             "type": 'Casual',
#                             "size": 'L',
#                             "manufacturer": 'Brand A',
#                             "productionDate": "2023-01-01",
#                             "price": 21.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/564x/d7/ab/de/d7abde31b08d7df15b1bb8e128a5697a.jpg'
#                         },
#                         {
#                             "id": 3,
#                             "name": 'Jeans',
#                             "description": 'Stylish blue jeans',
#                             "type": 'Casual',
#                             "size": 'L',
#                             "manufacturer": 'Brand B',
#                             "productionDate": "2023-01-01",
#                             "price": 49.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/564x/6f/c0/41/6fc041869320f5788bf2567eccd26d42.jpg'
#                         },
#                         {
#                             "id": 4,
#                             "name": 'Jeans',
#                             "description": 'Slim fit jeans',
#                             "type": 'Casual',
#                             "size": 'M',
#                             "manufacturer": 'Brand B',
#                             "productionDate": "2023-01-01",
#                             "price": 55.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/564x/bb/3d/a1/bb3da1fdd74be6f5768239d540562816.jpg'
#                         },
#                         {
#                             "id": 5,
#                             "name": 'Jacket',
#                             "description": 'Durable winter jacket',
#                             "type": 'Outerwear',
#                             "size": 'L',
#                             "manufacturer": 'Brand C',
#                             "productionDate": "2023-01-01",
#                             "price": 89.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/564x/12/2a/01/122a01af3961b972d8ac900c06016331.jpg'
#                         },
#                         {
#                             "id": 6,
#                             "name": 'Jacket',
#                             "description": 'Lightweight summer jacket',
#                             "type": 'Outerwear',
#                             "size": 'M',
#                             "manufacturer": 'Brand C',
#                             "productionDate": "2023-01-01",
#                             "price": 79.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/564x/00/09/98/0009981d72b2287af6987e2d1830f69a.jpg'
#                         },
#                         {
#                             "id": 7,
#                             "name": 'Sneakers',
#                             "description": 'Quality running sneakers',
#                             "type": 'Footwear',
#                             "size": '8',
#                             "manufacturer": 'Brand D',
#                             "productionDate": "2023-01-01",
#                             "price": 59.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/564x/24/d2/4d/24d24d34b24161598e108846dfe2ad56.jpg'
#                         },
#                         {
#                             "id": 8,
#                             "name": 'Sneakers',
#                             "description": 'Casual sneakers',
#                             "type": 'Footwear',
#                             "size": '9',
#                             "manufacturer": 'Brand D',
#                             "productionDate": "2023-01-01",
#                             "price": 65.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/564x/53/dd/2d/53dd2d5d755c2152f279121a58192657.jpg'
#                         },
#                         {
#                             "id": 9,
#                             "name": 'Dress',
#                             "description": 'Elegant evening dress',
#                             "type": 'Formal',
#                             "size": 'M',
#                             "manufacturer": 'Brand E',
#                             "productionDate": "2023-01-01",
#                             "price": 99.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/564x/13/d1/87/13d18728ea0ef62f9ac65da8e001c00e.jpg'
#                         },
#                         {
#                             "id": 10,
#                             "name": 'Dress',
#                             "description": 'Casual summer dress',
#                             "type": 'Formal',
#                             "size": 'S',
#                             "manufacturer": 'Brand E',
#                             "productionDate": "2023-01-01",
#                             "price": 79.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/564x/98/ad/1e/98ad1e225dcd906bb6d10909e124a796.jpg'
#                         },
#                         {
#                             "id": 11,
#                             "name": 'Cap',
#                             "description": 'Elegant and stylish hat.',
#                             "type": 'Accessories',
#                             "size": 'One Size',
#                             "manufacturer": 'Brand C',
#                             "productionDate": "2023-01-01",
#                             "price": 24.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/564x/c7/62/2e/c7622ed3f415431065f6deedf63040f6.jpg'
#                         },
#                         {
#                             "id": 12,
#                             "name": 'Cap',
#                             "description": 'Baseball cap',
#                             "type": 'Accessories',
#                             "size": 'One Size',
#                             "manufacturer": 'Brand F',
#                             "productionDate": "2023-01-01",
#                             "price": 19.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/564x/89/35/fa/8935fa7e830971d983652cf2a5f23faf.jpg'
#                         },
#                         {
#                             "id": 13,
#                             "name": 'Scarf',
#                             "description": 'Warm wool scarf',
#                             "type": 'Accessories',
#                             "size": 'One Size',
#                             "manufacturer": 'Brand F',
#                             "productionDate": "2023-01-01",
#                             "price": 29.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/564x/ac/01/51/ac0151cc41c379751acc0afa1c8d140e.jpg'
#                         },
#                         {
#                             "id": 14,
#                             "name": 'Scarf',
#                             "description": 'Lightweight summer scarf',
#                             "type": 'Accessories',
#                             "size": 'One Size',
#                             "manufacturer": 'Brand F',
#                             "productionDate": "2023-01-01",
#                             "price": 19.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/564x/9e/13/f6/9e13f6a90457ca77b1933ea3944c41a4.jpg'
#                         },
#                         {
#                             "id": 15,
#                             "name": 'Sunglasses',
#                             "description": 'Stylish sunglasses',
#                             "type": 'Accessories',
#                             "size": 'One Size',
#                             "manufacturer": 'Brand G',
#                             "productionDate": "2023-01-01",
#                             "price": 49.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/564x/bb/24/3f/bb243f50e3fa61538bac407885a9421c.jpg'
#                         },
#                         {
#                             "id": 16,
#                             "name": 'Watch',
#                             "description": 'Elegant wrist watch',
#                             "type": 'Accessories',
#                             "size": 'One Size',
#                             "manufacturer": 'Brand H',
#                             "productionDate": "2023-01-01",
#                             "price": 199.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/564x/44/f9/72/44f9721cbda958df0bfc823a595e12df.jpg'
#                         },
#                         {
#                             "id": 17,
#                             "name": 'Backpack',
#                             "description": 'Durable backpack',
#                             "type": 'Accessories',
#                             "size": 'One Size',
#                             "manufacturer": 'Brand I',
#                             "productionDate": "2023-01-01",
#                             "price": 79.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/564x/7a/4e/4b/7a4e4bc2ed991e4cc6c1330e2e4f9a8b.jpg'
#                         },
#                         {
#                             "id": 18,
#                             "name": 'Hat',
#                             "description": 'Stylish summer hat',
#                             "type": 'Accessories',
#                             "size": 'One Size',
#                             "manufacturer": 'Brand J',
#                             "productionDate": "2023-01-01",
#                             "price": 34.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/736x/15/eb/30/15eb309e8bbe27c3c3f458f47d6d1a25.jpg'
#                         },
#                         {
#                             "id": 19,
#                             "name": 'Belt',
#                             "description": 'Leather belt',
#                             "type": 'Accessories',
#                             "size": 'L',
#                             "manufacturer": 'Brand K',
#                             "productionDate": "2023-01-01",
#                             "price": 39.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/564x/cd/59/17/cd5917dc6a6fb5dd7df1e76dd5d73bbf.jpg'
#                         },
#                         {
#                             "id": 20,
#                             "name": 'Gloves',
#                             "description": 'Warm winter gloves',
#                             "type": 'Accessories',
#                             "size": 'M',
#                             "manufacturer": 'Brand L',
#                             "productionDate": "2023-01-01",
#                             "price": 14.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/564x/9f/22/54/9f225471b5865306a8d16cecdf3f2657.jpg'
#                         },
#                         {
#                             "id": 21,
#                             "name": 'Running Shoes',
#                             "description": 'Comfortable running shoes for daily wear',
#                             "type": 'Footwear',
#                             "size": 'L',
#                             "manufacturer": 'Brand C',
#                             "productionDate": "2023-01-01",
#                             "price": 49.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/564x/17/ed/84/17ed84133aa50a2a16317e89a68e643f.jpg'
#                         },
#                         {
#                             "id": 22,
#                             "name": 'T-Shirt',
#                             "description": 'Stylish casual shirt for everyday use',
#                             "type": 'Casual',
#                             "size": 'M',
#                             "manufacturer": 'Brand A',
#                             "productionDate": "2023-01-01",
#                             "price": 24.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/564x/cc/cf/11/cccf11391d8ef5d5ca4186d3a606f2a9.jpg'
#                         },
#                         {
#                             "id": 23,
#                             "name": 'Leather Jacket',
#                             "description": 'Durable and stylish leather jacket',
#                             "type": 'Outerwear',
#                             "size": 'XL',
#                             "manufacturer": 'Brand B',
#                             "productionDate": "2023-01-01",
#                             "price": 99.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/564x/31/a8/2a/31a82a3c0f2ae03053ae200462fe82bf.jpg'
#                         },
#                         {
#                             "id": 24,
#                             "name": 'Formal Shoes',
#                             "description": 'Elegant formal shoes for business occasions',
#                             "type": 'Footwear',
#                             "size": 'M',
#                             "manufacturer": 'Brand E',
#                             "productionDate": "2023-01-01",
#                             "price": 79.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/736x/cb/3a/8d/cb3a8dd97cc301e3d9b1fdbf9d1091e2.jpg'
#                         },
#                         {
#                             "id": 25,
#                             "name": 'Summer Dress',
#                             "description": 'Lightweight summer dress for casual outings',
#                             "type": 'Formal',
#                             "size": 'S',
#                             "manufacturer": 'Brand F',
#                             "productionDate": "2023-01-01",
#                             "price": 34.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/564x/62/58/cc/6258cc29d539d3c22ffb90aec89394c2.jpg'
#                         },
#                         {
#                             "id": 26,
#                             "name": 'Sneakers',
#                             "description": 'Trendy sneakers for everyday wear',
#                             "type": 'Footwear',
#                             "size": 'M',
#                             "manufacturer": 'Brand D',
#                             "productionDate": "2023-01-01",
#                             "price": 39.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/564x/32/a9/02/32a90221be0521fcf002296260956882.jpg'
#                         },
#                         {
#                             "id": 27,
#                             "name": 'T-Shirt',
#                             "description": 'Classic polo shirt for casual and semi-formal wear',
#                             "type": 'Casual',
#                             "size": 'L',
#                             "manufacturer": 'Brand A',
#                             "productionDate": "2023-01-01",
#                             "price": 29.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/564x/c9/24/52/c92452f990eb7f053baff6f360b4e6ef.jpg'
#                         },
#                         {
#                             "id": 28,
#                             "name": 'Denim Jeans',
#                             "description": 'Stylish denim jeans for everyday wear',
#                             "type": 'Casual',
#                             "size": 'M',
#                             "manufacturer": 'Brand B',
#                             "productionDate": "2023-01-01",
#                             "price": 59.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/564x/26/da/68/26da68d20f16eae3397551d7bce5683a.jpg'
#                         },
#                         {
#                             "id": 29,
#                             "name": 'Hiking Boots',
#                             "description": 'Durable hiking boots for outdoor adventures',
#                             "type": 'Footwear',
#                             "size": 'XL',
#                             "manufacturer": 'Brand C',
#                             "productionDate": "2023-01-01",
#                             "price": 89.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/564x/c2/94/12/c29412e984db1ad4b574ee401ba58153.jpg'
#                         },
#                         {
#                             "id": 30,
#                             "name": 'Beanie Hat',
#                             "description": 'Warm beanie hat for cold weather',
#                             "type": 'Accessories',
#                             "size": 'One Size',
#                             "manufacturer": 'Brand D',
#                             "productionDate": "2023-01-01",
#                             "price": 14.99,
#                             "reviews": [],
#                             "imageUrl": 'https://i.pinimg.com/564x/dd/67/a1/dd67a16b1a4b22ce939c78451ed6837e.jpg'
#                         }
#             # Add other items...
#         ]
#
#         matched_items = [item for item in clothing_items if product_name == item['name'].lower()]
#
#         if matched_items:
#                     item = matched_items[0]  # Return the exact match
#                     product_link = f"http://localhost:4200/clothing/{item['id']}"
#                     response_text = (
#                         f"We have the following {item['name']}: {item['description']}. "
#                         f"It's a {item['type']} product, available in size {item['size']}. "
#                         f"Manufactured by {item['manufacturer']}, produced on {item['productionDate']}. "
#                         f"The price is ${item['price']}. Product link: {product_link}"
#                     )
#
#
#
#
#                     dispatcher.utter_message(text=response_text)
#                     dispatcher.utter_message(image=item['imageUrl'])
#
#                     return []
#
#         dispatcher.utter_message(text=f"Sorry, we don't have information about {product_name}.")
#         return []


# from fastapi import APIRouter, HTTPException

# router = APIRouter()

# items = {
#     1: {"id": 1, "title": "Item One"},
#     2: {"id": 2, "title": "Item Two"},
#     3: {"id": 3, "title": "Item Three"},
# }


# @router.get("/items/{item_id}")
# async def read_item(item_id: int):
#     if item_id not in items:
#         raise HTTPException(status_code=404, detail="Item not founds")
#     return items[item_id]

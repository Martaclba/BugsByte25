def retrieve_overviews(conn, bundle_ids):
  if bundle_ids == []:
    return []
  
  with conn.cursor() as cur:
    print(f"SELECT bundle_id, name, description, image_url FROM bundles WHERE bundle_id IN ({','.join(str(id) for id in bundle_ids)})")
    cur.execute(f"SELECT bundle_id, name, description, image_url FROM bundles WHERE bundle_id IN ({','.join(str(id) for id in bundle_ids)})")
    bundles = cur.fetchall()
    print("argument bundles", len(bundle_ids))
    print("bundles", len(bundles))

    ans = {
      b[0]: { 
        "bundle_id": b[0],
        "name": b[1],
        "description": b[2],
        "image_url": b[3]
      }
      for b in bundles 
    }

    return [ans[id] for id in bundle_ids]
  

def retrieve_bundle(conn, bundle_id):
  with conn.cursor() as cur:
    cur.execute("SELECT bundle_id, name, description, instructions, image_url FROM bundles WHERE bundle_id = %s", bundle_id)
    b = cur.fetchall()[0]

    ans = {
      "bundle_id": b[0],
      "name": b[1],
      "description": b[2],
      "instructions": b[3],
      "image_url": b[4],
      "items": []
    }

    cur.execute("SELECT ingredient, quantity FROM bundle_items WHERE bundle_id = %s", ans['bundle_id'])
    items = cur.fetchall()

    for i in items:
      p = retrieve_product(cur, i[0])
      if p != None:
        ans['items'].append({ "quantity": i[1], "product": p })

    return ans

#Chooses the most relevant product based on the category
def retrieve_product(cur, ingredient):
  quot = '"'
  cur.execute(f"SELECT item_id, name, image_url FROM items WHERE {' AND '.join(f'name LIKE {quot}%{w}%{quot}' for w in ingredient.split(' '))} ORDER BY price_index ASC LIMIT 1")
  mproduct = cur.fetchall()
  print(mproduct)

  if len(mproduct) == 0:
    return None
  
  product = mproduct[0]
  return {
    "product_id": product[0],
    "name": product[1],
    "price": 0,
    "base_price": 0,
    "image_url": product[2]
  }
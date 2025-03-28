class Bundle {
  id: string;
  name: string;
  //code: number;
  description?: string;
  instructions?: string;
  items: BundleItem[];

  constructor(id: string, name: string, description: string, instructions: string, items: BundleItem[]) {
    this.id = id;
    this.name = name;
    this.description = description;
    this.instructions = instructions;
    this.items = items;
  }
}


class BundleItem {
  quantity: number;
  product: Product;

  constructor(product: Product, quantity: number) {
    this.product = product;
    this.quantity = quantity;
  }
}


//start/end date of discount
class Product {
  name: string;
  basePrice: number;
  price: number;
  image?: string;

  constructor(name: string, basePrice: number, price: number, image?: string) {
    this.name = name;
    this.price = price;
    this.basePrice = basePrice;
    this.image = image;
  }
}
export class BundleOverview {
  bundle_id: string;
  title: string;
  description?: string;
  image_url?: string;

  constructor(
    bundle_id: string,
    title: string,
    description?: string,
    image_url?: string
  ) {
    this.bundle_id = bundle_id;
    this.title = title;
    this.description = description;
    this.image_url = image_url;
  }
}

export class Bundle {
  bundle_id: string;
  title: string;
  description?: string;
  image_url?: string;
  //code: number;
  instructions?: string;
  items: BundleItem[];

  constructor(overview: BundleOverview, instructions?: string, items: BundleItem[]) {
    this.bundle_id = overview.bundle_id;
    this.title = overview.title;
    this.description = overview.description;
    this.image_url = overview.image_url;
    this.instructions = instructions;
    this.items = items;
  }
}

export class BundleItem {
  quantity: number;
  product: Product;

  constructor(product: Product, quantity: number = 1) {
    this.product = product;
    this.quantity = quantity;
  }
}

//start/end date of discount
export class Product {
  product_id: string;
  name: string;
  base_price: number;
  price: number;
  image_url?: string;

  constructor(product_id: string, name: string, base_price: number, price: number, image_url?: string) {
    this.product_id = product_id;
    this.name = name;
    this.price = price;
    this.base_price = base_price;
    this.image_url = image_url;
  }
}

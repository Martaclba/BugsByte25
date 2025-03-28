import { Bundle, BundleItem, BundleOverview, Product } from "./bundle";
import { User } from "./user";


async function user(id: string): Promise<User> {
  return new User("Joaquim", "joaquim01");
}

async function bundles(user_id: string): Promise<BundleOverview[]> {
  return [
    new BundleOverview("12345", "Arroz de Tomate", "yummy", "uwu"),
  ];
}

async function bundle(user_id: string, bundle_id: string): Promise<Bundle> {
  return new Bundle(new BundleOverview("12345", "Arroz de Tomate", "yummy", "uwu"), [
    new BundleItem(new Product("tomate", 1.01, 1.01), 2),
    new BundleItem(new Product("arroz", 2.01, 2.01)),
    new BundleItem(new Product("cebola", 2.01, 1.99)),
    new BundleItem(new Product("alho", 0.49, 0.49)),
  ]);
}
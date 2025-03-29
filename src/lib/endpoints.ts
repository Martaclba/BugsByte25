import { Bundle, BundleItem, BundleOverview, Product } from "./bundle";
import { User } from "./user";

export async function get_user(username: string): Promise<User> {
  let response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/users/${username}`);
  let data = await response.json();
  return data as User;
  
  return new User("Joaquim", "joaquim01");
}

export async function get_bundles(username: string): Promise<BundleOverview[]> {
  let response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/users/${username}/bundles`, );
  let data = await response.json();
  return data.bundles as BundleOverview[];

  return [
    new BundleOverview(
      "12345",
      "Picanha",
      "O arroz de tomate é um prato típico português, cremoso e aromático, feito com arroz cozido em molho de tomate temperado.",
      "asd"
    ),
    new BundleOverview(
      "12346",
      "Arroz",
      "O arroz de tomate é um prato típico português, cremoso e aromático, feito com arroz cozido em molho de tomate temperado.",
      "asd"
    ),
    new BundleOverview(
      "12347",
      "Arroz de Tomate",
      "O arroz de tomate é um prato típico português, cremoso e aromático, feito com arroz cozido em molho de tomate temperado.",
      "asd"
    ),
    new BundleOverview(
      "12348",
      "Feijao",
      "O arroz de tomate é um prato típico português, cremoso e aromático, feito com arroz cozido em molho de tomate temperado.",
      "asd"
    ),
    new BundleOverview(
      "12349",
      "Frango Churrasco",
      "O arroz de tomate é um prato típico português, cremoso e aromático, feito com arroz cozido em molho de tomate temperado.",
      "asd"
    ),
    new BundleOverview(
      "12340",
      "Pernil",
      "O arroz de tomate é um prato típico português, cremoso e aromático, feito com arroz cozido em molho de tomate temperado.",
      "asd"
    ),
  ];
}

export async function get_bundle(
  username: string,
  bundle_id: string
): Promise<Bundle> {
  let response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/users/${username}/bundles/${bundle_id}`);
  let data = await response.json();
  return data as Bundle;

  return new Bundle(
    new BundleOverview("12345", "Arroz de Tomate", "O arroz de tomate é um prato típico português, cremoso e aromático, feito com arroz cozido em molho de tomate temperado.", "asd"),
    [
      new BundleItem(new Product("1", "tomate", 1.01, 1.01), 2),
      new BundleItem(new Product("2", "arroz", 2.01, 2.01)),
      new BundleItem(new Product("3", "cebola", 2.01, 1.99)),
      new BundleItem(new Product("4", "alho", 0.49, 0.49)),
    ]
  );
}

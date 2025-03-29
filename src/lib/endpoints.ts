import { Bundle, BundleOverview } from "./bundle";
import { User } from "./user";

export async function get_user(username: string): Promise<User> {
  const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/users/${username}`);
  const data = await response.json();
  return data as User;
}

export async function get_bundles(username: string): Promise<BundleOverview[]> {
  const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/users/${username}/bundles`, );
  const data = await response.json();
  return data.bundles as BundleOverview[];
}

export async function get_bundle(
  username: string,
  bundle_id: string
): Promise<Bundle> {
  const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/users/${username}/bundles/${bundle_id}`);
  const data = await response.json();
  return data as Bundle;
}

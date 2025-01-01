import { checkAuth } from "$lib/auth";
import { redirect } from "@sveltejs/kit";

export const ssr = false;

export const load = async () => {
  const isAuthenticated = await checkAuth();
  if (!isAuthenticated) {
    throw redirect(302, "/login");
  }
};
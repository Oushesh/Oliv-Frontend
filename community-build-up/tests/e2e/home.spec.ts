import { expect, test } from "@playwright/test";

test("homepage loads and shows key marker", async ({ page }) => {
  await page.goto("/");

  await expect(page.getByRole("heading", { name: /longevity tracker/i })).toBeVisible();
  await expect(page.getByText(/track oxldl, apob,/i)).toBeVisible();
});

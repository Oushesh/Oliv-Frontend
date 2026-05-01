import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import Home from "@/app/page";

describe("Community Build Up homepage", () => {
  it("renders the main heading", () => {
    render(<Home />);

    expect(screen.getByRole("heading", { name: /longevity tracker/i })).toBeInTheDocument();
  });

  it("shows core biomarker sections", () => {
    render(<Home />);

    expect(screen.getAllByText(/oxldl/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/apob/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/hs-crp/i).length).toBeGreaterThan(0);
  });
});

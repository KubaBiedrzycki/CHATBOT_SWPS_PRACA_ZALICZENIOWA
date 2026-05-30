"use client";

import { useEffect } from "react";

/**
 * Loads Bootstrap's interactive JavaScript bundle (dropdowns, modals,
 * tooltips, etc.) on the client. The bundle includes Popper, so no
 * separate import is needed. Bootstrap's CSS is imported in layout.tsx.
 */
export default function BootstrapClient() {
  useEffect(() => {
    // @ts-expect-error — the prebuilt bundle has no bundled type declarations
    import("bootstrap/dist/js/bootstrap.bundle.min.js");
  }, []);

  return null;
}

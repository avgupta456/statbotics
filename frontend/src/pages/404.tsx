// pages/404.tsx
import React from "react";

import { useRouter } from "next/router";

// The useRouter hook for redirection
import NotFound from "../pagesContent/shared/notFound";

// Assuming you have a NotFound component

const NotFoundPage = () => {
  const router = useRouter();
  const path = router.asPath.split("/").filter(Boolean); // Extracts path segments

  // Handle redirection logic if necessary
  if (path.length === 1) {
    const firstPath = path[0];

    // Check if it's all digits
    if (/^\d+$/.test(firstPath)) {
      router.push(`/team/${firstPath}`);
    } else if (firstPath.includes("_")) {
      router.push(`/match/${firstPath}`);
    } else {
      router.push(`/event/${firstPath}`);
    }
  }

  return <NotFound type="Page" />;
};

export default NotFoundPage;

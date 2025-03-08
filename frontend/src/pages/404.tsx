// pages/404.tsx
import React, { useEffect } from "react";

import { useRouter } from "next/router";

import NotFound from "../pagesContent/shared/notFound";

const NotFoundPage = () => {
  const router = useRouter();
  const path = router.asPath.split("/").filter(Boolean);

  useEffect(() => {
    if (path.length === 1) {
      const firstPath = path[0];

      if (/^\d+$/.test(firstPath)) {
        router.replace(`/team/${firstPath}`);
      } else if (firstPath.includes("_")) {
        router.replace(`/match/${firstPath}`);
      } else {
        router.replace(`/event/${firstPath}`);
      }
    }
  }, [path, router]);

  return <NotFound type="Page" />;
};

export default NotFoundPage;

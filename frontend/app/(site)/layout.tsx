"use client";

import React, { createContext, useState } from "react";

export const AppContext = createContext({
  team: 0,
  setTeam: (team: number) => {},
});

export default function Layout({ children }: { children: React.ReactNode }) {
  const [team, setTeam] = useState(0);

  return <AppContext.Provider value={{ team, setTeam }}>{children}</AppContext.Provider>;
}

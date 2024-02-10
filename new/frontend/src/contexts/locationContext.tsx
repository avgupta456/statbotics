import { createContext, useContext } from "react";

export const LocationContext = createContext({
  location: null,
  setLocation: () => {},
} as {
  location: string | null;
  // eslint-disable-next-line no-unused-vars
  setLocation: (value: string | null) => void;
});

export const useLocation = () => {
  const context = useContext(LocationContext);
  if (context === undefined) {
    throw new Error("useData must be used within a LocationProvider");
  }
  return context;
};

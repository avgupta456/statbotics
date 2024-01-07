/* eslint-disable no-unused-vars */

/* eslint-disable @typescript-eslint/no-unused-vars */
import { createContext, useContext } from "react";

export const PreferencesContext = createContext({
  EPACellFormat: "full_error_bars",
  setEPACellFormat: (EPACellFormat: string) => {},
} as {
  EPACellFormat: string;
  setEPACellFormat: any;
});

export const usePreferences = () => {
  const context = useContext(PreferencesContext);
  if (context === undefined) {
    throw new Error("usePreferences must be used within a PreferencesProvider");
  }
  return context;
};

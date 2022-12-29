import React from "react";
import { components } from "react-select";

import { Category10Colors } from "../constants";

export const Option = ({ children, ...props }) => {
  const { onMouseMove, onMouseOver, ...rest } = props.innerProps;
  const newProps: any = Object.assign(props, { innerProps: rest });
  return <components.Option {...newProps}>{children}</components.Option>;
};

export const multiSelectStyles = (getIndex: any) => ({
  menu: (provided) => ({ ...provided, zIndex: 9999 }),
  multiValue: (styles, { data }: { data: any }) => {
    const index = getIndex(data.value) % Category10Colors.length;
    return {
      ...styles,
      backgroundColor: Category10Colors[index],
    };
  },
  multiValueLabel: (styles, { data }) => ({
    ...styles,
    color: "#eee",
  }),
  multiValueRemove: (styles, { data }) => ({
    ...styles,
    color: "#eee",
    ":hover": {
      color: "black",
    },
  }),
});

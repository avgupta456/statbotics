import React from "react";
import { components } from "react-select";

export const Option = ({ children, ...props }) => {
  const { ...rest } = props.innerProps;
  // Currently does nothing, can be used to remove props from innerProps
  // const { onMouseMove, onMouseOver, ...rest } = props.innerProps;
  const newProps: any = Object.assign(props, { innerProps: rest });
  return <components.Option {...newProps}>{children}</components.Option>;
};

export const Category10Colors = [
  "#1f77b4",
  "#ff7f0e",
  "#2ca02c",
  "#d62728",
  "#9467bd",
  "#8c564b",
  "#e377c2",
  "#7f7f7f",
  "#bcbd22",
  "#17becf",
];

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

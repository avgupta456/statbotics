import React from "react";
import { classnames } from "../../utils";

const Button = (props) => {
  return (
    <button
      {...props}
      className={classnames(
        "my-4 mx-2 p-2 rounded",
        "text-sm md:text-md lg:text-lg font-semibold",
        props.className
      )}
    >
      {props.children}
    </button>
  );
};

export default Button;

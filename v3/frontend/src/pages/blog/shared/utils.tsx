/* eslint-disable react/no-children-prop */
import "katex/dist/katex.min.css";
import rehypeKatex from "rehype-katex";
import remarkMath from "remark-math";

import ReactMarkdown from "react-markdown";

export const renderMath = (str: string) => {
  return (
    <ReactMarkdown
      //inline
      className="inline-block m-0 not-prose"
      children={`$${str}$`}
      remarkPlugins={[remarkMath]}
      rehypePlugins={[rehypeKatex]}
    />
  );
};

export const renderMathBlock = (str: string) => {
  return (
    <ReactMarkdown
      className="w-full text-center"
      children={`$$${str}$$`}
      remarkPlugins={[remarkMath]}
      rehypePlugins={[rehypeKatex]}
    />
  );
};

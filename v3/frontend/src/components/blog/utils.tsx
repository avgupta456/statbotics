/* eslint-disable react/no-children-prop */
import ReactMarkdown from "react-markdown";

import "katex/dist/katex.min.css";
import rehypeKatex from "rehype-katex";
import remarkMath from "remark-math";

export const renderMath = (str: string) => (
  <ReactMarkdown
    // inline
    className="not-prose m-0 inline-block"
    children={`$${str}$`}
    remarkPlugins={[remarkMath]}
    rehypePlugins={[rehypeKatex]}
  />
);

export const renderMathBlock = (str: string) => (
  <ReactMarkdown
    className="w-full text-center"
    children={`$$${str}$$`}
    remarkPlugins={[remarkMath]}
    rehypePlugins={[rehypeKatex]}
  />
);

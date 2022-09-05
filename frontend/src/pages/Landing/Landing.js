/* eslint-disable react/jsx-one-expression-per-line */

import React from "react";

import { Link } from "react-router-dom";

import { Button } from "../../components";
import { classnames } from "../../utils";

const Highlight = (props) => {
  return (
    <div
      {...props}
      className={classnames(
        "leading-tight rounded px-1 bg-gradient-to-r cursor-pointer hover:ring-2",
        props.className
      )}
    >
      {props.children}
    </div>
  );
};

const LandingScreen = () => {
  return (
    <section>
      <div
        className={classnames(
          "w-full min-h-screen -mt-16",
          "bg-gradient-to-br from-red-200 to-blue-400 text-gray-800 flex flex-wrap"
        )}
      >
        <div className='w-full flex flex-col justify-center p-4 lg:p-12'>
          <div
            className={classnames(
              "text-center text-white text-lg md:text-3xl lg:text-5xl 2xl:text-6xl leading-relaxed md:leading-relaxed lg:leading-relaxed 2xl:leading-relaxed font-bold",
              "w-full mx-auto mb-6 flex flex-col"
            )}
          >
            <div>Level up your scouting team with</div>
            <div className='flex flex-row justify-center items-center'>
              <Highlight className='from-violet-500 to-violet-400 hover:from-blue-500 hover:to-violet-500 hover:ring-violet-400'>
                predictive
              </Highlight>
              {", "}
              <Highlight className='ml-1 from-green-500 to-green-400 hover:from-cyan-500 hover:to-green-500 hover:ring-cyan-500'>
                intuitive
              </Highlight>
              {", and "}
              <Highlight className='ml-1 from-rose-500 to-rose-400 hover:from-orange-500 hover:to-rose-500 hover:ring-rose-500'>
                accessible
              </Highlight>
            </div>
            <div>FRC ratings and predictions</div>
          </div>
          <div className='w-full flex flex-wrap justify-center'>
            <Link to='/paper' className='w-auto'>
              <Button className='bg-gray-100 hover:bg-gray-300'>
                Read the White Paper
              </Button>
            </Link>
            <Link to='/users' className='w-auto'>
              <Button className='bg-blue-500 hover:bg-blue-600 text-white'>
                Go to Dashboard
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
};

export default LandingScreen;

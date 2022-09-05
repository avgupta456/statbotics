import React from "react";

import { Link } from "react-router-dom";

const NoMatchScreen = () => {
  return (
    <div className='h-full w-full flex flex-col justify-center items-center'>
      <div className='flex p-8'>
        <div className='hidden md:block pr-8 text-5xl font-semibold text-blue-500'>
          404
        </div>
        <div className='flex flex-col'>
          <div className='md:pl-8 md:border-l-2 md:border-gray-200'>
            <div className='text-4xl md:text-5xl font-bold text-gray-900'>
              Page not Found
            </div>
            <div className='text-lg text-gray-500 my-4'>
              Please check the URL in the address bar and try again.
            </div>
            <Link to='/'>
              <button className='py-2 px-6 rounded-sm bg-blue-500 hover:bg-blue-600 text-lg text-white'>
                Go to Home
              </button>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NoMatchScreen;

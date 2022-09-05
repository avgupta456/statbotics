import React, { useState } from "react";

import { Link } from "react-router-dom";

import { GiHamburgerMenu as HamburgerIcon } from "react-icons/gi";

import StatboticsIcon from "../../assets/favicon.ico";
import { classnames } from "../../utils";

const Header = () => {
  const [toggle, setToggle] = useState(false);

  return (
    <div className='text-gray-100 bg-gray-800 shadow-md body-font sticky top-0 z-50'>
      <div className='p-5 flex flex-wrap'>
        {/* Statbotics Logo */}
        <Link
          to='/'
          className='flex items-center title-font font-medium text-white mb-0 md:mr-8'
        >
          <img src={StatboticsIcon} alt='logo' className='w-6 h-6' />
          <span className='ml-2 text-xl'>Statbotics</span>
        </Link>
        {/* Pages: Wrapped, Dashboard, Demo */}
        <div className='hidden md:flex'></div>
        {/* Hamburger Menu */}
        <div className='md:hidden flex ml-auto items-center'>
          <button
            type='button'
            className='outline-none'
            onClick={() => setToggle(!toggle)}
          >
            <HamburgerIcon className='w-6 h-6 text-white' />
          </button>
        </div>
      </div>
      {/* Hamburger Dropdown */}
      <div className={classnames("p-5 pt-0", !toggle && "hidden")}></div>
    </div>
  );
};

export default Header;

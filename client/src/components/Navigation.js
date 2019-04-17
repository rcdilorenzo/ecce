import React from 'react';
import { NavLink, Link } from 'react-router-dom';
import PageWrapper from './PageWrapper';

const Navigation = () => {
  return (
    <nav className="w-full nav-bg">
      <div className="max-w-lg mx-auto flex items-center pl-3 pr-3">
        <h1 className="flex-no-grow">
          <Link to="/" className="text-white no-underline">Ecce</Link>
        </h1>
        <ul className="nav-list flex-grow ml-5">
          <li>
            <NavLink
              activeClassName="nav-list__block-link--active"
              className="nav-list__block-link"
              to="/verses">Verses</NavLink>
          </li>
          <li>
            <NavLink
              activeClassName="nav-list__block-link--active"
              className="nav-list__block-link"
              to="/topics">Topics</NavLink>
          </li>
          <li>
            <NavLink
              activeClassName="nav-list__block-link--active"
              className="nav-list__block-link"
              to="/about">About</NavLink>
          </li>
        </ul>
        <div className="flex-no-grow invisible sm:visible">
          <ul className="nav-list">
            <li>
              <a className="nav-list__social-link"
                href="https://github.com/rcdilorenzo">
                <span className="fab fa-github-alt"></span>
              </a>
            </li>
            <li>
              <a className="nav-list__social-link"
                href="https://www.linkedin.com/in/christian-di-lorenzo-518545184/">
                <span className="fab fa-linkedin"></span>
              </a>
            </li>
            <li>
              <a className="nav-list__social-link"
                href="https://twitter.com/rcdilorenzo">
                <span className="fab fa-twitter"></span>
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;

import React from 'react';
import { Link } from 'react-router-dom';

const Footer = props => (
  <footer>
    <div className="max-w-lg mx-auto p-3 pt-4 pb-10 text-white flex flex-wrap">
      <p className="flex-grow mr-2">
        <Link to="/about" className="text-white no-underline">Christian Di Lorenzo</Link> &#169; 2019
      </p>
      <p className="text-right">
        Crafted with <a href="https://keras.io">Keras</a>, <a href="https://reactjs.org">React</a>, and more.
      </p>
    </div>
  </footer>
);

export default Footer;

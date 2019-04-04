import React from 'react';
import * as R from 'ramda';

const Card = ({ children }) =>  {
  const className = [
    'flex-1',
    'flex-no-shrink',
    'm-2',
    'p-8',
    'bg-grey-lighter',
    'rounded-lg',
    'shadow-md',
    'md:w-64'
  ].join(' ');

  return (
    <div className={className}>
      {children}
    </div>
  );
};

export default Card;

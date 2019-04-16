import React from 'react';

const Card = ({ children }) =>  {
  const className = [
    'flex-1',
    'flex-no-shrink',
    'm-2',
    'p-8',
    'bg-subtle',
    'rounded-lg',
    'shadow-md',
    'md:w-1/2',
    'card'
  ].join(' ');

  return (
    <div className={className}>
      {children}
    </div>
  );
};

export default Card;

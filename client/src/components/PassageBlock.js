import React from 'react';

const PassageBlock = ({ name, references, text }) => (
  <article className="pt-2 pb-2">
    <h3>{name}</h3>
    <p>{text}</p>
  </article>
);

export default PassageBlock;

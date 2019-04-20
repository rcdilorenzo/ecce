import React, { useState } from 'react';
import * as R from 'ramda';

const renderContent = ({ open, name, references, text }) => (
  <React.Fragment>
    <header className="list-item__title">{name}</header>
    {!open && references.length > 1 && <p className="list-item__details">
      {references.length} verses
    </p>}
    {open && <div className="list-item__body pt-3">
      {text.split('\n').map((t, i) => (<p key={i}>{t}</p>))}
    </div>}
  </React.Fragment>
);

const PassageBlock = (props) => {
  const [open, setOpen] = useState(false);

  if (props.linkOnly) {
    return (
      <a className="list-item cursor-pointer"
        href={`https://www.biblegateway.com/passage/?search=${props.name}&version=ESV`}
        target={'_blank'}>
        {renderContent({ ...props, open })}
      </a>
    );
  }

  return (
    <article className="list-item cursor-pointer" onClick={() => setOpen(!open)}>
      {renderContent({ ...props, open })}
    </article>
  )
};

export default PassageBlock;

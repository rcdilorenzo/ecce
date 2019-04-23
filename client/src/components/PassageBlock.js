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
  const [open, setOpen] = useState(props.open || false);

  if (!props.open && props.linkOnly) {
    return (
      <a className="list-item cursor-pointer"
        href={`https://www.biblegateway.com/passage/?search=${props.name}&version=ESV`}
        target={'_blank'}>
        {renderContent({ ...props, open })}
      </a>
    );
  }

  const className = props.open ? `list-item list-item--no-hover` : `list-item cursor-pointer`;

  return (
    <article className={className} onClick={() => props.open || setOpen(!open)}>
      {renderContent({ ...props, open })}
    </article>
  )
};

export default PassageBlock;

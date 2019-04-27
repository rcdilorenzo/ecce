import React, { useState } from 'react';
import BibleGatewayLink, { READ_MORE_STYLE } from './BibleGatewayLink';

import * as Passage from '../models/passage';

const renderContent = ({ open, linkOnly, passage }) => (
  <React.Fragment>
    <header className="list-item__title">{passage.name}</header>
    {!open && passage.references.length > 1 && <p className="list-item__details">
      {passage.references.length} verses
    </p>}
    <div className={`list-item__body ${open ? 'pt-3' : ''}`}>
      {open && Passage.lines(passage).map((t, i) => (<p key={i}>{t}</p>))}
      {!linkOnly && open &&
        <BibleGatewayLink passage={passage} style={READ_MORE_STYLE} text="Read more" />}
    </div>
  </React.Fragment>
);

const PassageBlock = (props) => {
  const [open, setOpen] = useState(props.open || false);

  if (!props.open && props.linkOnly) {
    return (
      <BibleGatewayLink passage={props.passage} className="list-item cursor-pointer">
        {renderContent({ ...props, open })}
      </BibleGatewayLink>
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

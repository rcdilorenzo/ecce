import React, { useState } from 'react';

import PassageBlock from '../PassageBlock';
import BibleGatewayLink, { READ_MORE_STYLE } from '../BibleGatewayLink';
import * as Reference from '../../models/reference';
import * as Passage from '../../models/passage';

const renderPassage = (passage, index) => (
  <PassageBlock key={index} open={true} passage={passage} />
);

const PassageGroupBlock = ({ cluster: { uuid, reference, passages }, open, opening }) => {
  const passage = Reference.toPassage(reference);
  const toggle = () => opening(ref, open ? null : uuid);
  const [ref, setRef] = useState(null);

  return (
    <div>
      <button className="list-item cursor-pointer w-full" onClick={toggle}>
        <div className="flex flex-row items-center w-full" ref={setRef}>
          <div className="w-full">
            <header className="list-item__title">{passage.name}</header>
            <div className="list-item__body pt-3">
              {Passage.lines(passage).map((t, i) => (<p key={i}>{t}</p>))}
            </div>
            <BibleGatewayLink passage={passage} style={READ_MORE_STYLE} text="Read more" />
          </div>
          <div className="ml-2 text-grey">
            <span className={`fas fa-lg fa-angle-${open ? 'down' : 'right'} p-1`}>
            </span>
          </div>
        </div>
      </button>

      {open && <div className="pb-3 pt-2">
        <p className="pb-1 pl-2 text-xs uppercase">Related Passages</p>
        {passages.map(renderPassage)}
        <button className="text-center text-sm w-full pt-1 cursor-pointer" onClick={toggle}>Collapse</button>
       </div>}
    </div>
  );
};

export default PassageGroupBlock;

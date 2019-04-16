import React, { useState } from 'react';


const PassageBlock = ({ name, references, text }) => {
  const [open, setOpen] = useState(false);

  return (
    <article className="list-item cursor-pointer" onClick={() => setOpen(!open)}>
      <h3 className="list-item__title">{name}</h3>
      {!open && <p className="list-item__detail">{references.length} verses</p>}
      {open && <div className="list-item__body pt-3">
        {text.split('\n').map((t, i) => (<p key={i}>{t}</p>))}
       </div>}
    </article>
  )
};

export default PassageBlock;

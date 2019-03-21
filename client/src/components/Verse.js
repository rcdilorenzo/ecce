import React, { useState, useEffect } from 'react'

import * as ESV from '../models/esv';

const Verse = ({ book, chapter, verse }) => {
  const [text, setText] = useState('');

  useEffect(() => {
    ESV.text(book, chapter, verse).then(setText)
  }, [book, chapter, verse, setText])

  if (text) {
    return (<p className="italic mb-5">{text}</p>);
  } else {
    return (<p className="italic mb-5">Loading {book} {chapter}:{verse}</p>);
  }
};

export default Verse;

import React, { useState, useEffect } from 'react';
import Verse from './Verse';
import Maybe from 'folktale/maybe';

import * as R from 'ramda';
import * as Nave from '../models/nave';

const renderTopics = (topics) => {
  return topics.map(({ topic_name, category_text, subtopic_text}, index) => {
    return (
        <li key={index}>{topic_name}, {category_text}, {subtopic_text}</li>
    );
  });
}

const VerseTopics = ({ book, chapter, verse }) => {
  const [topics, setTopics] = useState(Maybe.Nothing());

  useEffect(() => {
    Nave
      .topics(book, chapter, verse)
      .then(R.pipe(Maybe.Just, setTopics))
  }, [book, chapter, verse, setTopics]);

  return topics.matchWith({
    Nothing: () => (<p>Loading topics for {book} {chapter}:{verse}</p>),
    Just: ({ value }) => {
      return (
        <div>
          <h2 className="pt-5 pb-5">{`${book} ${chapter}:${verse}`}</h2>
          <Verse book={book} chapter={chapter} verse={verse} />
          <ul>{renderTopics(value)}</ul>
        </div>
      );
    }
 });
};

export default VerseTopics;

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import VerseText from './VerseText';
import Maybe from 'folktale/maybe';

import * as R from 'ramda';
import * as Nave from '../../models/nave';

const renderTopics = (topics) => {
  return topics.map(({ topic_name, category_text, subtopic_text}, index) => {
    return (
      <li key={index}>
        <Link to={`/topics?q=${topic_name}`}>{topic_name}</Link>
        <span>, {category_text}, {subtopic_text}</span>
      </li>
    );
  });
}

const VerseTopics = ({ book, chapter, verse }) => {
  const [topics, setTopics] = useState(Maybe.Nothing());

  useEffect(() => {
    Nave
      .topics(book, chapter, verse)
      .then(R.tap(console.log))
      .then(R.pipe(Maybe.Just, setTopics))
  }, [book, chapter, verse, setTopics]);

  return topics.matchWith({
    Nothing: () => (<p>Loading topics for {book} {chapter}:{verse}</p>),
    Just: ({ value }) => {
      return (
        <div>
          <h2>{`${book} ${chapter}:${verse}`}</h2>
          <VerseText book={book} chapter={chapter} verse={verse} />
          <ul>{renderTopics(value)}</ul>

          <footnote className="block pt-5 italic text-right">
            <a href="https://www.esv.org/resources/esv-global-study-bible/copyright-page/"
              className="no-underline text-black">
              <span className="underline">English Standard Version</span><sup>&#169;</sup>
            </a>
          </footnote>
        </div>
      );
    }
 });
};

export default VerseTopics;

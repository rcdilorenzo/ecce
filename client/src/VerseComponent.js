import React, { Component } from 'react';

import esv from './data/ESV.json';

const renderTopics = (topics) => {
  return topics.map(({ topic_name, category_text, subtopic_text}, index) => {
    return (
        <li key={index}>{topic_name}, {category_text}, {subtopic_text}</li>
    );
  });
}

const VerseComponent = ({ book, chapter, verse, topics }) => {
  return (
    <div>
      <h2 className="pt-5 pb-5">{`${book} ${chapter}:${verse}`}</h2>
      <p className="italic mb-5">
        {esv[book][chapter][verse]}
      </p>
      <ul>{renderTopics(topics)}</ul>
    </div>
  );
};

export default VerseComponent;

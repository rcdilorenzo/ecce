import React, { Component } from 'react';

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
      <h1>{`${book} ${chapter}:${verse}`}</h1>
      <ul>{renderTopics(topics)}</ul>
    </div>
  );
};

export default VerseComponent;

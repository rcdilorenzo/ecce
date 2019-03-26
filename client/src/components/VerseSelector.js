import React from 'react';
import Async from 'react-async';
import Select from 'react-select';
import * as R from 'ramda';

import * as ESV from '../models/esv';

const toOptions = (value) => {
  return { value, label: value };
};

const VerseSelector = ({ book, chapter, verse, handlers, references }) => {
  const bookOptions = ESV.books.map(toOptions);

  return (
    <div className="flex flex-wrap max-w-sm m-auto">
      <Select
        className="flex-grow w-48 pr-2 mb-2"
        value={toOptions(book)}
        options={bookOptions}
        onChange={handlers.bookSelected} />

      <Select
        className="pr-2 w-24 mb-2"
        value={toOptions(chapter)}
        options={R.map(toOptions, Object.keys(references[book]))}
        onChange={handlers.chapterSelected} />

      <Select
        className="w-24 mb-2"
        value={toOptions(verse)}
        options={R.map(toOptions, references[book][chapter])}
        onChange={handlers.verseSelected} />
    </div>
  )
}

const AsyncVerseSelector = (props) => (
  <Async promiseFn={ESV.references}>
    <Async.Loading>
      <div className="flex flex-wrap max-w-sm m-auto">
        <Select
          className="flex-grow w-48 pr-2 mb-2"
          defaultValue={toOptions('Loading...')}
          options={[]} />

        <Select
          className="pr-2 w-24 mb-2"
          defaultValue={toOptions('...')}
          options={[]} />

        <Select
          className="w-24 mb-2"
          defaultValue={toOptions('...')}
          options={[]} />
      </div>
    </Async.Loading>

    <Async.Resolved>
      {data => <VerseSelector {...props} references={data} />}
    </Async.Resolved>
  </Async>
)

export default AsyncVerseSelector;

import React from 'react';
import Async from 'react-async';
import AsyncError from './AsyncError';
import Select from 'react-select';
import * as R from 'ramda';

import * as ESV from '../models/esv';

const toOptions = (value) => {
  return { value, label: value };
};

const mapToOptions = R.map(toOptions);

const VerseSelector = ({ book, chapter, verse, handlers, references }) => {
  return (
    <div className="flex flex-wrap max-w-sm m-auto">
      <Select
        className="flex-grow w-48 pr-2 mb-2"
        value={toOptions(book)}
        options={mapToOptions(ESV.books)}
        onChange={handlers.bookSelected} />

      <Select
        className="pr-2 w-24 mb-2"
        value={toOptions(chapter)}
        options={mapToOptions(ESV.chapters(references, book))}
        onChange={handlers.chapterSelected} />

      <Select
        className="w-24 mb-2"
        value={toOptions(verse)}
        options={mapToOptions(ESV.verses(references, book, chapter))}
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

    <AsyncError />
  </Async>
)

export default AsyncVerseSelector;

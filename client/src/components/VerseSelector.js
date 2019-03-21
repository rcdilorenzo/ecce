import React from 'react';
import Select from 'react-select';
import AsyncSelect from 'react-select/lib/Async';
import * as R from 'ramda';

import * as ESV from '../models/esv';

const toOptions = (value) => {
  return { value, label: value };
};

const VerseSelector = ({ book, chapter, verse, handlers }) => {
  const bookOptions = ESV.books.map(toOptions);

  return (
    <div className="flex flex-wrap">
      <Select
        className="flex-grow w-48 pr-2 mb-2"
        value={toOptions(book)}
        options={bookOptions}
        onChange={handlers.bookSelected} />

      <AsyncSelect
        className="pr-2 w-24 mb-2"
        defaultOptions
        value={toOptions(chapter)}
        loadOptions={() => ESV.chapters(book).then(R.map(toOptions))}
        onChange={handlers.chapterSelected} />

      <AsyncSelect
        className="w-24 mb-2"
        value={toOptions(verse)}
        defaultOptions
        loadOptions={() => ESV.verses(book, chapter).then(R.map(toOptions))}
        onChange={handlers.verseSelected} />
    </div>
  )
}

export default VerseSelector;

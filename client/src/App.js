import React, { Component } from 'react';
import * as R from 'ramda';
import Select from 'react-select';
import AsyncSelect from 'react-select/lib/Async';

import * as ESV from './models/esv';

import VerseTopics from './components/VerseTopics';

const toOptions = (value) => {
  return { value, label: value };
};

class App extends Component {
  constructor(props) {
    super(props);
    this.bookOptions = ESV.books.map(toOptions);

    this.state = {
      book: ESV.books[0],
      chapter: 1,
      verse: 1
    }
  }

  bookSelected(selected) {
    const book = selected.value;
    this.setState(prevState => ({ ...prevState, book, chapter: 1, verse: 1 }));
  }

  chapterSelected(selected) {
    const chapter = selected.value;
    this.setState(prevState => ({ ...prevState, chapter, verse: 1 }));
  }

  verseSelected(selected) {
    const verse = selected.value;
    this.setState(prevState => ({ ...prevState, verse }));
  }

  render() {
    const { book, chapter, verse } = this.state;
    return (
      <div className="p-5 max-w-sm m-auto mt-5">
        <h1 className="pt-5 pb-5">Verse Topic Explorer</h1>
        <div className="flex flex-wrap">
          <Select
            className="flex-grow w-48 pr-2 mb-2"
            value={toOptions(book)}
            options={this.bookOptions}
            onChange={this.bookSelected.bind(this)} />

          <AsyncSelect
            className="pr-2 w-24 mb-2"
            defaultOptions
            value={toOptions(chapter)}
            loadOptions={() => ESV.chapters(book).then(R.map(toOptions))}
            onChange={this.chapterSelected.bind(this)} />

          <AsyncSelect
            className="w-24 mb-2"
            value={toOptions(verse)}
            defaultOptions
            loadOptions={() => ESV.verses(book, chapter).then(R.map(toOptions))}
            onChange={this.verseSelected.bind(this)} />
          </div>
        <div>
        <VerseTopics {...this.state} />
        </div>
      </div>
    );
  }
};

export default App;

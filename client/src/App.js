import React, { Component } from 'react';
import * as R from 'ramda';
import Select from 'react-select';
import Maybe from 'folktale/maybe';

import VerseComponent from './VerseComponent';
import { CANONICAL_ORDER } from './constants';
import naveReference from './data/nave-by-reference.json';

class App extends Component {
  constructor(props) {
    super(props);
    this.bookOptions = CANONICAL_ORDER.map(this._valueToOptions);

    this.state = {
      book: CANONICAL_ORDER[0],
      chapter: 1,
      verse: 1
    }
  }

  _valueToOptions(value) {
    return { value, label: value };
  }

  chapters(book) {
    return Object.keys(naveReference[book]);
  }

  verses(book, chapter) {
    return Object.keys(naveReference[book][chapter]);
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
            value={this._valueToOptions(book)}
            options={this.bookOptions}
            onChange={this.bookSelected.bind(this)} />
          <Select
            className="pr-2 w-24"
            value={this._valueToOptions(chapter)}
            options={this.chapters(book).map(this._valueToOptions)}
            onChange={this.chapterSelected.bind(this)} />
          <Select
            className="w-24"
            value={this._valueToOptions(verse)}
            options={this.verses(book, chapter).map(this._valueToOptions)}
            onChange={this.verseSelected.bind(this)} />
          </div>
        <div>
          <VerseComponent {...this.state}
            topics={naveReference[book][chapter][verse]} />
        </div>
      </div>
    );
  }
};

export default App;

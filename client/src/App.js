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
    const reference = naveReference;
    debugger;
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
      <div>
        <Select
          value={this._valueToOptions(book)}
          options={this.bookOptions}
          onChange={this.bookSelected.bind(this)} />
        <Select
          value={this._valueToOptions(chapter)}
          options={this.chapters(book).map(this._valueToOptions)}
          onChange={this.chapterSelected.bind(this)} />
        <Select
          value={this._valueToOptions(verse)}
          options={this.verses(book, chapter).map(this._valueToOptions)}
          onChange={this.verseSelected.bind(this)} />
        <div>
          <VerseComponent {...this.state}
            topics={naveReference[book][chapter][verse]} />
        </div>
      </div>
    );
  }
};

export default App;

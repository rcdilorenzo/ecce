import React, { Component } from 'react';
import * as R from 'ramda';

import * as ESV from './models/esv';
import VerseTopics from './components/VerseTopics';
import VerseSelector from './components/VerseSelector';
import TopicExplorer from './components/TopicExplorer';

const mergeRight = R.flip(R.merge);

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      book: ESV.books[0], chapter: 1, verse: 1
    };
  }

  bookSelected(selected) {
    this.setState(mergeRight({ book: selected.value, chapter: 1, verse: 1 }));
  }

  chapterSelected(selected) {
    this.setState(mergeRight({ chapter: selected.value, verse: 1 }));
  }

  verseSelected(selected) {
    this.setState({ verse: selected.value });
  }

  render() {
    const selectionHandlers = {
      bookSelected: this.bookSelected.bind(this),
      chapterSelected: this.chapterSelected.bind(this),
      verseSelected: this.verseSelected.bind(this)
    };

    return (
      <div className="p-5 max-w-lg m-auto mt-5">
        <h1 className="pt-5 pb-5">Verse Topic Explorer</h1>
        <VerseSelector
          {...this.state}
          handlers={selectionHandlers} />

        <VerseTopics {...this.state} />

        <h1 className="pt-5 pb-5">Topic Explorer</h1>
        <TopicExplorer />
      </div>
    );
  }
};

export default App;

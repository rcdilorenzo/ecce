import React, { Component } from 'react';
import * as R from 'ramda';

import * as ESV from './models/esv';
import * as Data from './models/data';
import VerseTopics from './components/VerseTopics';
import VerseSelector from './components/VerseSelector';
import NaveExplorer from './components/NaveExplorer';
import Dashboard from './components/Dashboard';
import Card from './components/Card';
import TopicCountByVerse from './components/cards/TopicCountByVerse';
import VerseCountByTopic from './components/cards/VerseCountByTopic';

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
      <div className="mt-8">
        <h1 className="pb-3 text-center">
          <a className="no-underline text-black" href="https://github.com/rcdilorenzo/ecce">
            Ecce - Exploratory Core Concept Extraction
          </a>
        </h1>
        <Dashboard>
          <Card>
            <VerseSelector {...this.state} handlers={selectionHandlers} />
            <VerseTopics {...this.state} />
          </Card>
          <Card>
            <NaveExplorer />
          </Card>
          <Card>
            <TopicCountByVerse />
          </Card>
          <Card>
            <VerseCountByTopic />
          </Card>
        </Dashboard>
      </div>
    );
  }
};

export default App;

import React, { Component } from 'react';
import * as R from 'ramda';

import * as ESV from '../../models/esv';
import VerseTopics from '../verse/VerseTopics';
import VerseSelector from '../verse/VerseSelector';
import NaveExplorer from '../topic/NaveExplorer';
import Dashboard from '../Dashboard';
import Card from '../Card';
import TopicCountByVerse from '../eda/TopicCountByVerse';
import VerseCountByTopic from '../eda/VerseCountByTopic';

const mergeRight = R.flip(R.merge);

class Index extends Component {
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
    );
  }
};

export default Index;

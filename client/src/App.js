import React, { Component } from 'react';
import * as R from 'ramda';
import Tab from '@bit/semantic-org.semantic-ui-react.tab';

import * as ESV from './models/esv';
import VerseTopics from './components/VerseTopics';
import VerseSelector from './components/VerseSelector';
import NaveExplorer from './components/NaveExplorer';

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

    const panes = [
        { menuItem: 'Verse Explorer', render: () => {
            return (
            <Tab.Pane attached={false}>
                <VerseSelector {...this.state} handlers={selectionHandlers} />
                <VerseTopics {...this.state} />
            </Tab.Pane>
            );
        } },
        { menuItem: "Nave's Topics Explorer", render: () => {
            return (
            <Tab.Pane attached={false}>
                <NaveExplorer />
            </Tab.Pane>
            );
        } }
    ]

    return (
      <div className="p-5 max-w-lg m-auto mt-5">
        <Tab menu={{ attached: false }} panes={panes} />
      </div>
    );
  }
};

export default App;

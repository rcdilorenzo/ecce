import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import * as R from 'ramda';

import * as ESV from '../../models/esv';

import VerseTopics from '../VerseTopics';
import VerseSelector from '../VerseSelector';
import PageWrapper from '../PageWrapper';

const mergeRight = R.flip(R.merge);

class Verses extends Component {
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
    this.setState(mergeRight({ chapter: selected.value, verse: 1 }));}

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
      <PageWrapper>
        <Helmet>
          <title>Ecce - Verses</title>
        </Helmet>

        <h1 className="mb-3">
          <a href="https://www.esv.org/resources/esv-global-study-bible/copyright-page/"
            className="no-underline text-black">
            English Standard Version &#169;
          </a>
        </h1>

        <VerseSelector {...this.state} handlers={selectionHandlers} />
        <VerseTopics {...this.state} />
      </PageWrapper>
    );
  }
};

export default Verses;

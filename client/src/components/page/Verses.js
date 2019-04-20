import React from 'react';
import { Helmet } from 'react-helmet-async';

import VerseExplorer from '../verse/VerseExplorer';
import PageWrapper from '../PageWrapper';

const Verses = _props => (
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

    <VerseExplorer />
  </PageWrapper>
);

export default Verses;

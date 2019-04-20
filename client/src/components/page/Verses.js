import React from 'react';
import { Helmet } from 'react-helmet-async';

import VerseExplorer from '../verse/VerseExplorer';
import PageWrapper from '../PageWrapper';

const Verses = _props => (
  <PageWrapper>
    <Helmet>
      <title>Ecce - Verses</title>
    </Helmet>

    <h1>Explore Verses</h1>
    <VerseExplorer />
  </PageWrapper>
);

export default Verses;

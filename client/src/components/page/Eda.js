import React from 'react';
import { Helmet } from 'react-helmet-async';

import PageWrapper from '../PageWrapper';
import Card from '../Card';

import NaveExplorer from '../topic/NaveExplorer';
import TopicCountByVerse from '../eda/TopicCountByVerse';
import VerseCountByTopic from '../eda/VerseCountByTopic';

const currentDimensions = () => {
  const innerHeight = window.innerHeight;
  const innerWidth = window.innerWidth;
  return {
    height: Math.min(400, innerHeight / 3),
    width: Math.min(724, innerWidth - 90)
  };
};

const captionStyle = 'italic block text-sm mt-2';

const EDA = (props) => (
  <PageWrapper>
    <Helmet>
      <title>Ecce - EDA</title>
    </Helmet>

    <h1>Exploratory Data Analysis</h1>

    <Card>
      <NaveExplorer dimensions={currentDimensions} />
      <caption className={captionStyle}>
        Topics and categories from Nave's Topical Index
      </caption>
    </Card>

    <Card>
      <TopicCountByVerse />
      <caption className={captionStyle}>
        Number of verses per topic
      </caption>
    </Card>

    <Card>
      <VerseCountByTopic />
      <caption className={captionStyle}>
        Number of topics per verses
      </caption>
    </Card>
  </PageWrapper>
);

export default EDA;

import React from 'react';
import { Helmet } from 'react-helmet-async';

import PageWrapper from '../PageWrapper';
import Card from '../Card';

import VerseExplorer from '../verse/VerseExplorer';
import NaveExplorer from '../topic/NaveExplorer';
import TopicCountByVerse from '../eda/TopicCountByVerse';
import VerseCountByTopic from '../eda/VerseCountByTopic';

const About = (props) => (
  <PageWrapper>
    <Helmet>
      <title>Ecce - About</title>
    </Helmet>

    <h1>About</h1>
    <p>Work in progress...</p>

    <Card><VerseExplorer /></Card>

    <Card><NaveExplorer /></Card>

    <Card><TopicCountByVerse /></Card>

    <Card><VerseCountByTopic /></Card>
  </PageWrapper>
);

export default About;

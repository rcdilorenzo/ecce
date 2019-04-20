import React from 'react';
import { Helmet } from 'react-helmet-async';

import PageWrapper from '../PageWrapper';

const About = (props) => (
  <PageWrapper>
    <Helmet>
      <title>Ecce - About</title>
    </Helmet>

    <h1>About</h1>
    <p>Work in progress...</p>
  </PageWrapper>
);

export default About;

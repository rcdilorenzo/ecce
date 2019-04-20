import React, { useEffect, useState } from 'react';
import * as R from 'ramda';

import * as ESV from '../../models/esv';
import PageWrapper from '../PageWrapper';
import TopicResults from '../ai/TopicResults';
import PassageResults from '../ai/PassageResults';

const mergeRight = R.flip(R.merge);

const Index = props => (
  <PageWrapper>
    <h1 className="pt-3 text-center">Bible Text AI</h1>
    <p className="text-center">
      Type any text and we'll find related Biblical topics and verses
    </p>
    <textarea
      placeholder="e.g. God does not need our approval for his decisions."
      className="search w-full" style={{ marginBottom: '0.5rem' }}
      name="search" type="text" />
    <button className="search-button italic">Coming soon...</button>

    <div className="md:flex flex-column">
      <article className="flex-grow">
        <TopicResults />
      </article>
      <article className="flex-grow md:ml-2">
        <PassageResults />
      </article>
    </div>
  </PageWrapper>
);

export default Index;

import React, { useEffect, useState } from 'react';
import * as R from 'ramda';

import LoadingIndicator from 'react-loading-indicator';

import * as ESV from '../../models/esv';
import PageWrapper from '../PageWrapper';
import TopicResults from '../ai/TopicResults';
import PassageResults from '../ai/PassageResults';

const mergeRight = R.flip(R.merge);

const messages = [
  'Browsing through 856 topics',
  'Performing forward propagation',
  'Examining term frequencies',
  'Looking through 65,000+ verse groups',
  'Vectorizing text for supervised clustering',
  'Warming up the gerbils for work',
  'Flipping pages faster than a sword drill',
  'Examining your theological tendencies',
  'Incorporating verses for your journey'
];

let timer = null;
let lastMessage = null;
const selectMessage = (setMessage) => {
  let message = lastMessage;
  while (message === lastMessage) {
    message = messages[Math.floor(Math.random() * messages.length)]
  }

  setMessage(message);
  lastMessage = message;
};


const Index = props => {
  const [isLoading, _setIsLoading] = useState(false);
  const [text, setText] = useState('');
  const [loadingMessage, setMessage] = useState('');

  const _match = (text) => {
    if (isLoading) {
      return;
    }

    if (timer) {
      clearInterval(timer);
    }

    timer = setInterval(() => selectMessage(setMessage), 2500);
    selectMessage(setMessage);
    _setIsLoading(true);
  };

  return (
    <PageWrapper>
      <h1 className="pt-3 text-center">Bible Text AI</h1>
      <p className="text-center">
        Type any text and we'll find related Biblical topics and verses
      </p>
      <textarea
        placeholder="e.g. God does not need our approval for his decisions."
        className="search w-full"
        value={text}
        onChange={e => isLoading || setText(e.target.value)}
        style={{ marginBottom: '0.5rem' }}
        name="search" type="text" />


      <button
        className="search-button"
        onClick={() => _match(text)}>
        {!isLoading && 'Find'}
        {isLoading && <>
          <LoadingIndicator />
          <span
            class="inline-block align-top pl-2"
            style={{ paddingTop: '1px' }}>
            {loadingMessage}...
          </span>
        </>}
      </button>

      <div className="md:flex flex-column">
        <article className="flex-grow">
          <TopicResults />
        </article>
        <article className="flex-grow md:ml-2">
          <PassageResults />
        </article>
      </div>
    </PageWrapper>
  )
}

export default Index;

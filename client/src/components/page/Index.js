import React, { useEffect, useState } from 'react';
import * as R from 'ramda';

import LoadingIndicator from 'react-loading-indicator';

import * as Ai from '../../models/ai';
import * as ESV from '../../models/esv';
import * as Nave from '../../models/nave';
import * as Passage from '../../models/passage';
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
  'Warming up the gerbils for work', 'Flipping pages faster than a sword drill',
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

const runPrediction = (setResults, setIsLoading, setError, text) => {
  Ai.predict(text)
    .then(results => {
      setIsLoading(false);
      setResults({ ...results, autoExpand: true });
    })
    .catch(error => {
      console.log(error);
      setIsLoading(false);
      setError('Failed. Please try again later.');
    });
};


const Index = props => {
  const [isLoading, setIsLoading] = useState(false);
  const [text, setText] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const [results, setResults] = useState({ topics: [], passages: [], autoExpand: false });

  useEffect(() => {
    Promise.all([
      Nave.topicNodes({ limit: 10 }),
      Passage.defaultPassages()
    ]).then(([topics, passages]) =>
      setResults({ topics, passages })
    );
  }, setResults);

  const _match = (text) => {
    if (isLoading) {
      return;
    }

    if (text.split(' ').length < 5) {
      return setError('Please enter a sentence with at least five words')
    } else {
      setError(null);
    }

    if (timer) {
      clearInterval(timer);
    }

    timer = setInterval(() => selectMessage(setMessage), 2500);
    selectMessage(setMessage);
    setIsLoading(true);

    runPrediction(setResults, setIsLoading, setError, text);
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
        onChange={e => isLoading || setError(null) || setText(e.target.value.replace(/\n$/, ''))}
        onKeyUp={e => e.key === 'Enter' && _match(text)}
        style={{ marginBottom: '0.5rem' }}
        name="search" type="text" />

      {error && error.length > 0 && <p className="text-red text-center pb-2">
        {error}
      </p>}

      <button
        className="search-button"
        onClick={() => _match(text)}>
        {!isLoading && 'Find'}
        {isLoading && <>
          <LoadingIndicator />
          <span
            className="inline-block align-top pl-2"
            style={{ paddingTop: '1px' }}>
            {message}...
          </span>
        </>}
      </button>

      <div className="md:flex flex-column">
        <article className="flex-grow" style={{ minWidth: '300px' }}>
          <TopicResults data={results.topics}/>
        </article>
        <article className="flex-grow md:ml-2">
          <PassageResults data={results.passages} autoExpand={results.autoExpand} />
        </article>
      </div>
    </PageWrapper>
  )
}

export default Index;

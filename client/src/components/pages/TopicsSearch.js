import React, { useState, useEffect } from 'react';
import * as R from 'ramda';
import * as Nave from '../../models/nave';
import qs from 'query-string';

import TopicSearchResult from '../TopicSearchResult';

const paramsQuery = R.pipe(
  R.prop('location'),
  R.prop('search'),
  qs.parse,
  R.propOr('', 'q')
);

const updateQuery = R.curry((setResults, newQuery) => {
  Nave.topicNodes({ query: newQuery }).then(setResults);
});

const queryInputChanged = R.curry((setQuery, setResults, event) => {
  const newQuery = event.target.value;
  setQuery(newQuery);
  updateQuery(setResults, newQuery);
});

const TopicsSearch = (props) => {
  const [query, setQuery] = useState(paramsQuery(props));
  const [results, setResults] = useState([{ placeholder: true }])

  useEffect(() => {
    updateQuery(setResults, query)
  }, [setResults]);

  return (
    <div className="mx-auto">
      <main className="max-w-lg mx-auto">
        <h1 className="pt-3">Search Topics</h1>
        <input
          className="w-full p-3 mt-3 mb-5 rounded-lg border border-black focus:border-blue-dark outline-none"
          name="search" type="text" value={query}
          onChange={queryInputChanged(setQuery, setResults)} />
        <article className="pb-10">
          {results.map(r => <TopicSearchResult {...r} />)}
        </article>
      </main>
    </div>
  )
};

export default TopicsSearch;

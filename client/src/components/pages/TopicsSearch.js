import React, { useState, useEffect } from 'react';
import * as R from 'ramda';
import * as Nave from '../../models/nave';
import { Redirect } from 'react-router-dom';
import qs from 'query-string';

import PageWrapper from '../PageWrapper';
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
  const [results, setResults] = useState([{ id: 'placeholder', placeholder: true }])

  useEffect(() => {
    updateQuery(setResults, query)
  }, [setResults]);

  if (results.length === 1 && paramsQuery(props) === query && !results[0].placeholder) {
    return (<Redirect to={`/topics/${results[0].id}`} />)
  }

  return (
    <PageWrapper>
      <h1 className="pt-3">Search Topics</h1>
      <input
        className="search w-full"
        name="search" type="text" value={query}
        onChange={queryInputChanged(setQuery, setResults)} />
      <article className="pb-10">
        {results.map(r => <TopicSearchResult key={r.id} {...r} />)}
      </article>
    </PageWrapper>
  )
};

export default TopicsSearch;

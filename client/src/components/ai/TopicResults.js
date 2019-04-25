import React from 'react';
import LoadingIndicator from 'react-loading-indicator';

import TopicSearchResult from '../topic/TopicSearchResult';

const TopicResults = ({ data }) => (
  <React.Fragment>
    <h2>Topics</h2>
    {data.length === 0 && <p className="list-item">
      <LoadingIndicator />
      <span className="ml-2">Loading</span>
    </p>}
    {data.length > 0 && data.map(r =>
      <TopicSearchResult key={r.id} openNewTab={true} {...r} />
    )}
  </React.Fragment>
);

export default TopicResults;

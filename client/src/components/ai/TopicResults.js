import React, { useEffect, useState } from 'react';

import * as Nave from '../../models/nave';
import TopicSearchResult from '../topic/TopicSearchResult';

const TopicResults = props => {
  const [results, setResults] = useState([{ id: 'placeholder', placeholder: true }]);

  useEffect(() => {
    Nave.topicNodes({ limit: 10 }).then(setResults);
  }, setResults);

  return (
    <React.Fragment>
      <h2>Topics</h2>
      {results.map(r => <TopicSearchResult key={r.id} {...r} />)}
    </React.Fragment>
  );
};

export default TopicResults;

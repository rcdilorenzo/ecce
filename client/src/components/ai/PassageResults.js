import React, { useEffect, useState } from 'react';

import * as Passage from '../../models/passage';
import TopicSearchResult from '../topic/TopicSearchResult';
import PassageBlock from '../PassageBlock';

const PassageResults = props => {
  const [results, setResults] = useState([{ name: 'Loading...', references: [], text: '' }]);

  useEffect(() => {
    Passage.defaultPassages().then(setResults);
  }, setResults);

  return (
    <React.Fragment>
      <h2>Passages</h2>
      {results.map(p => <PassageBlock key={p.name} linkOnly={true} {...p} />)}
    </React.Fragment>
  );
};

export default PassageResults;

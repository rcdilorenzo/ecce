import React, { useState, useEffect } from 'react';
import * as R from 'ramda';
import { TagCloud } from 'react-tagcloud';

import * as Nave from '../models/nave';

const topicCloud = R.pipe(
  Object.entries,
  R.map(([ value, count ]) => ({ value, count: Math.log2(count) }))
);

const cloudStyles = {
  maxHeight: '400px',
  overflow: 'scroll',
  padding: '10px',
  backgroundColor: '#3e3833'
};

const TopicExplorer = React.memo((_props) => {
  const [topicCounts, setTopicCounts] = useState({});

  useEffect(() => {
    Nave
      .topicCounts()
      .then(setTopicCounts);
  }, [setTopicCounts])

  console.log('re-render topics')

  return (
    <div>
      <div style={cloudStyles}>
        <TagCloud minSize={5}
          maxSize={30}
          tags={topicCloud(topicCounts)}
          onClick={tag => alert(`'${tag.value}': ${topicCounts[tag.value]} verses`)} />
      </div>
    </div>
  )
});

export default TopicExplorer;

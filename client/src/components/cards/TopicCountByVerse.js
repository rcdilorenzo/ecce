import React, { useEffect, useState } from 'react';
import { VictoryChart, VictoryBar, VictoryAxis } from 'victory';
import * as R from 'ramda';

import * as Data from '../../models/data';

const TopicCountByVerse = (props) => {
  const [data, setData] = useState([{ topics: 0, frequency: 0 }]);

  useEffect(() => {
    Data.stats().then(R.pipe(R.prop('topics'), setData));
  }, [setData]);

  return (
    <React.Fragment>
      <h2>Topic Count By Verse</h2>
      <div style={{ height: '300px' }}>
        <VictoryChart height={300} padding={{ left: 75, right: 50, top: 50, bottom: 50}}>
          <VictoryBar data={data} x="topics" y="frequency" />
          <VictoryAxis label="Number of Topics" />
          <VictoryAxis dependentAxis={true} style={{ axisLabel: { padding: 60 }}} label="Number of Verses" />
        </VictoryChart>
      </div>
    </React.Fragment>
  );
};

export default TopicCountByVerse;

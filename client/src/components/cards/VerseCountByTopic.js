import React, { useEffect, useState } from 'react';
import { VictoryChart, VictoryBar, VictoryLine, VictoryAxis } from 'victory';
import * as R from 'ramda';
import { kde, kernels, hist } from '../../models/stats';
import * as Data from '../../models/data';

const min = R.reduce(R.min, 0);
const max = R.reduce(R.max, 1);

const VerseCountByTopic = (props) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    Data.stats().then(R.pipe(
      R.prop('verses'),
      setData
    ));
  }, [setData]);

  const verseCount = R.filter(x => x > 50, R.map(R.prop('verse_count'), data));

  const height = 300;
  const barWidth = 10;
  const kdeMultiplier = 100000;
  const f = kde(kernels.gaussian, 0.4, verseCount);
  const domain = { x: [min(verseCount), max(verseCount)] };
  const padding = { left: 75, right: 50, top: 50, bottom: 50 };
  const bin = hist().domain(domain.x).thresholds(30);

  return (
    <React.Fragment>
      <h2>Verse Count By Topic</h2>
        <div style={{ height: `${height}px` }}>
          <VictoryChart height={height} domain={domain} padding={padding} scale={{ y: 'sqrt' }}>
            <VictoryBar
              data={bin(verseCount)}
              alignment="start"
              barWidth={barWidth}
              x="x0"
              y="length" />

            <VictoryLine
              y={R.pipe(R.prop('x'), f, R.multiply(kdeMultiplier))}
              samples={100}
              style={{ data: { stroke: "red" } }} />

            <VictoryAxis label="Number of Verses per Topic" />

            <VictoryAxis
              dependentAxis={true}
              style={{ axisLabel: { padding: 60 }}}
              label="Frequency of Topics" />
          </VictoryChart>
        </div>
    </React.Fragment>
  );
};

export default VerseCountByTopic;

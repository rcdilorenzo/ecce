import React, { useEffect, useState } from 'react';
import { VictoryChart, VictoryBar, VictoryLine, VictoryAxis } from 'victory';
import { kde, kernels, hist } from '../../models/stats';
import Slider, { Handle } from 'rc-slider';
import Tooltip from 'rc-tooltip';
import 'rc-slider/assets/index.css';
import * as R from 'ramda';
import * as Data from '../../models/data';

const min = R.reduce(R.min, 0);
const max = R.reduce(R.max, 1);

const handle = (props) => {
  const { value, dragging, index, ...restProps } = props;
  return (
    <Tooltip
      prefixCls="rc-slider-tooltip"
      overlay={value}
      visible={dragging}
      placement="top"
      key={index} >

      <Handle value={value} {...restProps} />
    </Tooltip>
  );
};

const VerseCountByTopic = (props) => {
  const [data, setData] = useState([]);
  const [minCount, setMinCount] = useState(30);

  useEffect(() => {
    Data.stats().then(R.pipe(
      R.prop('verses'),
      setData
    ));
  }, [setData]);

  const verseCount = R.filter(
    x => x >= minCount,
    R.map(R.prop('verse_count'), data)
  );

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

      <p className="italic pt-3 pb-3 text-sm">
        Filtering topics with at least {minCount} verses ({verseCount.length} of {data.length} topics)
      </p>

      <Slider
        step={2}
        min={0}
        max={200}
        marks={{ 0: 0, 50: 50, 100: 100, 150: 150, 200: 200 }}
        handle={handle}
        defaultValue={minCount}
        onAfterChange={setMinCount} />

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

          <VictoryAxis label="Verses per Topic" />

          <VictoryAxis
            dependentAxis={true}
            style={{ axisLabel: { padding: 60 }}}
            label="# Topics" />
        </VictoryChart>
      </div>
    </React.Fragment>
  );
};

export default VerseCountByTopic;

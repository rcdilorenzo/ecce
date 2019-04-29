import React, { useState } from 'react';
import Async from 'react-async';
import { VictoryChart, VictoryBar, VictoryLine, VictoryAxis } from 'victory';
import Slider, { Handle } from 'rc-slider';
import Tooltip from 'rc-tooltip';
import AsyncError from '../AsyncError';
import * as R from 'ramda';
import 'rc-slider/assets/index.css';

import { kde, kernels, hist } from '../../models/stats';

const min = values => R.reduce(R.min, R.head(values) || 0, values);
const max = values => R.reduce(R.max, R.head(values) || 1, values);

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

const TopicVerseHistogram = ({
  kdeMultiplier, xAxisLabel, yAxisLabel, bandwidth, sliderMarks, sliderMax,
  title, defaultMinCount, barWidth, binCount, data, attr, filterDescription
}) => {

  const [minCount, setMinCount] = useState(defaultMinCount);

  const counts = R.filter(
    x => x >= minCount, data
  );

  const height = 300;
  const f = kde(kernels.gaussian, bandwidth, counts);
  const domain = { x: [min(counts), max(counts)] };
  const padding = { left: 75, right: 50, top: 50, bottom: 50 };
  const bin = hist().domain(domain.x).thresholds(binCount);

  return (
    <React.Fragment>
      <h2>{title}</h2>

      <p className="italic pt-3 pb-3 text-sm">
        {filterDescription(minCount, counts, data)}
      </p>

      <Slider
        step={1}
        min={1}
        max={sliderMax}
        marks={sliderMarks}
        handle={handle}
        defaultValue={minCount}
        onAfterChange={setMinCount} />

      <div style={{ height: `${height}px` }}>
        <VictoryChart height={height} width={600} domain={domain} padding={padding} scale={{ y: 'sqrt' }}>
          <VictoryBar
            data={bin(counts)}
            alignment="start"
            barWidth={barWidth}
            x="x0"
            y="length" />

          <VictoryLine
            y={R.pipe(R.prop('x'), f, R.multiply(kdeMultiplier))}
            samples={100}
            style={{ data: { stroke: "red" } }} />

          <VictoryAxis label={xAxisLabel} />

          <VictoryAxis
            dependentAxis={true}
            style={{ axisLabel: { padding: 60 }}}
            label={yAxisLabel} />
        </VictoryChart>
      </div>
    </React.Fragment>
  );
};

const AsyncTopicVerseHistogram = (props) => (
  <Async promiseFn={() => props.promise().then(R.map(R.prop(props.attr)))}>
    <Async.Loading>
      <h2>{props.title}</h2>
      <p className="italic text-sm pt-3">Loading graph...</p>
    </Async.Loading>

    <Async.Resolved>
      {data => <TopicVerseHistogram {...props} data={data} />}
    </Async.Resolved>

    <AsyncError />
  </Async>
);

export default AsyncTopicVerseHistogram;

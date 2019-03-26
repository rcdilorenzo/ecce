import React, { useState, useEffect } from 'react';
import * as Nave from '../models/nave';
import * as R from 'ramda';
import Select from 'react-select';

import NaveTopicGraph from './NaveTopicGraph';

const MAX_TOPICS = 800;

const sortTopics = R.sortBy(R.pipe(R.prop('reference_count'), R.negate));

const loadData = (setData) => {
  Nave
    .topicNodes()
    .then(sortTopics)
    .then(topics => setData({ selected: topics[0], topics }));
};

const toOptions = t => {
  return { value: t.id, label: `${t.label} (${t.reference_count} verses)` };
};

const options = R.pipe(
  R.prop('topics'),
  R.take(MAX_TOPICS),
  R.map(toOptions)
);

const selectedOption = R.curry((data, setData, option) => {
  return setData(R.over(
    R.lens(R.prop('topics'), R.assoc('selected')),
    R.find(t => t.id === option.value),
    data
  ));
});


const NaveExplorer = React.memo((_props) => {
    const [data, setData] = useState({ topics: [], selected: null });
    useEffect(() => loadData(setData), [setData])

    if (data.topics.length === 0) {
        return (<p>Loading...</p>);
    }

    console.log(data)

    return (
      <React.Fragment>
        <Select className="pr-2 mb-2"
          value={toOptions(data.selected)}
          options={options(data)}
          onChange={selectedOption(data, setData)} />

        <NaveTopicGraph
          topicId={data.selected.id}
          topicName={data.selected.label} />
      </React.Fragment>
    );
});

export default NaveExplorer;



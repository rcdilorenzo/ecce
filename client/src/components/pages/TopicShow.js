import React from 'react';
import Async from 'react-async';
import * as R from 'ramda';

import AsyncError from '../AsyncError';
import PageWrapper from '../PageWrapper';
import NaveTopicGraph from '../NaveTopicGraph';
import PassageBlock from '../PassageBlock';

import * as Nave from '../../models/nave';

const topicId = R.view(R.lensPath(['match', 'params', 'topicId']));

const graphWidth = () => {
  const innerWidth = window.innerWidth;
  return Math.min(800, innerWidth - 40);
};

const TopicShow = props => {
  const { id, label } = props;
  console.log(props);
  return (
    <PageWrapper>
      <h1 className="pt-3 pb-3">{label}</h1>
      <div className="bg-grey-light">
        <NaveTopicGraph
          width={graphWidth}
          topicId={id}
          topicName={label} />
      </div>
      <section>
        <h2 className="pt-3 pb-3">Passages</h2>
        {props.passages.map((p, i) => <PassageBlock key={i} {...p} /> )}
      </section>
    </PageWrapper>
  );
};

const loadData = (props) => {
  return Promise.all([
    Nave.topic(topicId(props), { references: false }),
    Nave.topicPassages(topicId(props))
  ]).then(results => ({
    ...results[0], passages: results[1]
  }));
};

const AsyncTopicShow = (props) => (
  <Async promiseFn={() => loadData(props)}>
    <Async.Loading>
      <p>Loading graph...</p>
    </Async.Loading>

    <Async.Resolved>
      {data => <TopicShow {...props} {...data} />}
    </Async.Resolved>

    <AsyncError />
  </Async>
);

export default React.memo(AsyncTopicShow);

import React from 'react';
import Async from 'react-async';
import AsyncError from '../AsyncError';
import PageWrapper from '../PageWrapper';
import NaveTopicGraph from '../NaveTopicGraph';

import * as Nave from '../../models/nave';

const graphWidth = () => {
  const innerWidth = window.innerWidth;
  return Math.min(800, innerWidth - 40);
};

const TopicShow = props => {
  const { id, label } = props;
  return (
    <PageWrapper>
      <h1 className="pt-3 pb-3">{label}</h1>
      <div className="bg-grey-light">
        <NaveTopicGraph
          width={graphWidth}
          topicId={id}
          topicName={label} />
      </div>
    </PageWrapper>
  );
};

const AsyncTopicShow = (props) => (
  <Async promiseFn={() => Nave.topic(props.match.params.topicId, { references: false })}>
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

import React, { useState, useEffect } from 'react';
import Async from 'react-async';
import { ForceGraph2D } from 'react-force-graph';

import * as Nave from '../../models/nave';
import AsyncError from '../AsyncError';


const graphData = ({ topicId, topicName, categories }) => ({
  nodes: [{
      id: topicId,
      label: topicName,
      level: 'topic',
      reference_count: 800
    }].concat(
      categories.map(c => ({
        ...c,
        level: 'category'
      }))
    ),
  links: categories.map(c => ({
    source: c.topic_id,
    target: c.id
  }))
});


const nodeCanvasObject = (node, ctx, globalScale) => {
  const label = node.label;
  const fontSize = Math.max(6, 4 * Math.log10(node.reference_count)) / globalScale;
  ctx.font = `${fontSize}px Sans-Serif`;

  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillStyle = 'rgba(0, 0, 0, 1)';
  ctx.fillText(label, node.x, node.y);
};

const currentDimensions = () => {
  const innerHeight = window.innerHeight;
  const innerWidth = window.innerWidth;
  return {
    height: Math.min(400, innerHeight / 3),
    width: Math.min(774, innerWidth - 40)
  };
};


const NaveTopicGraph = (props) => {
  const dimensionFunction = props.dimensions ? props.dimensions : currentDimensions;
  const [dimensions, setDimensions] = useState(dimensionFunction());

  useEffect(() => {
    window.addEventListener('resize', () => {
      setDimensions(dimensionFunction());
    }, false);
  }, [setDimensions]);

  return (
      <ForceGraph2D
        width={dimensions.width}
        height={dimensions.height}
        linkHoverPrecision={1}
        graphData={graphData(props)}
        dagMode={'radialout'}
        dagLevelDistance={250}
        linkColor={() => 'rgba(0,0,0,0.2)'}
        nodeRelSize={2}
        nodeVal={n => Math.sqrt(n.reference_count)}
        nodeLabel="label"
        nodeCanvasObject={nodeCanvasObject}
        nodeAutoColorBy="level"
        d3VelocityDecay={0.3} />
  );
};

const AsyncNaveTopicGraph = (props) => (
  <Async promiseFn={() => Nave.categoryNodes(props.topicId)}>
    <Async.Loading>
      <p>Loading graph...</p>
    </Async.Loading>

    <Async.Resolved>
      {data => <NaveTopicGraph {...props} categories={data} />}
    </Async.Resolved>

    <AsyncError />
  </Async>
);

export default React.memo(AsyncNaveTopicGraph);

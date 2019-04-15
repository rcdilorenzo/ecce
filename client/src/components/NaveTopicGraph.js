import React, { useState, useEffect } from 'react';
import Async from 'react-async';
import { ForceGraph2D } from 'react-force-graph';

import * as Nave from '../models/nave';
import AsyncError from './AsyncError';


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
  const textWidth = ctx.measureText(label).width;
  // some padding
  const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2);

  /* ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
   * ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);*/
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillStyle = 'rgba(0, 0, 0, 1)';
  ctx.fillText(label, node.x, node.y);
};

const currentWidth = () => {
  const innerWidth = window.innerWidth;
  return innerWidth >= 768 ? (innerWidth / 2 - 105) : (innerWidth - 135)
};


const NaveTopicGraph = (props) => {
  const widthFunction = props.width ? props.width : currentWidth;
  const [width, setWidth] = useState(widthFunction());

  useEffect(() => {
    window.addEventListener('resize', () => {
      setWidth(widthFunction());
    }, false);
  }, [setWidth]);

  return (
      <ForceGraph2D
        width={width}
        height={400}
        graphData={graphData(props)}
        dagMode={'radialout'}
        dagLevelDistance={300}
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

import React from 'react';
import { ForceGraph2D } from 'react-force-graph';

const NaveTopicGraph = ({ topicId, topicName, categories }) => {
  const topicNode = { id: topicId, label: topicName, level: 'topic', reference_count: 800 };

  const graphData = {
    nodes: [topicNode].concat(categories.map(c => ({  ...c, level: 'category' }))),
    links: categories.map(c => ({ source: c.topic_id, target: c.id}))
  };

  const width = Math.min(window.innerWidth - 95, 670);

  return (
      <ForceGraph2D
        width={width}
        height={400}
        graphData={graphData}
        dagMode={'radialout'}
        dagLevelDistance={300}
        linkColor={() => 'rgba(0,0,0,0.1)'}
        nodeRelSize={2}
        nodeVal={n => Math.sqrt(n.reference_count)}
        nodeLabel="label"
        nodeCanvasObject={(node, ctx, globalScale) => {
            const label = node.label;
            const fontSize = Math.max(6, 4*(Math.log10(node.reference_count)))/globalScale;
            ctx.font = `${fontSize}px Sans-Serif`;
            const textWidth = ctx.measureText(label).width;
            const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2); // some padding
            ctx.fillStyle = 'rgba(250, 250, 250, 0.5)';
            ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillStyle = node.color;
            ctx.fillText(label, node.x, node.y);
        }}
        nodeAutoColorBy="level"
        d3VelocityDecay={0.3} />
  );
};

export default NaveTopicGraph;

import React, { useState, useEffect } from 'react';
import * as R from 'ramda';
import * as Nave from '../models/nave';
import { ForceGraph2D } from 'react-force-graph';

const loadData = (setData) => {
  Promise.all([
    Nave.topicNodes(),
    Nave.categoryNodes(),
    Nave.subtopicNodes()
  ]).then(([topics, categories, subtopics]) => {
    const filteredTopics = topics.filter(t => t.reference_count > 800);
    const topicIds = filteredTopics.map(t => t.id);

    const filteredCategories = categories.filter(
      c => topicIds.includes(c.topic_id)
    );
    const categoryIds = filteredCategories.map(c => c.id);
    const filteredSubtopics = subtopics.filter(
      st => st.category_id && categoryIds.includes(st.category_id)
    );

    const nodes = filteredTopics
      .concat(filteredCategories)
      .concat(filteredSubtopics);

    const links = (filteredCategories.map(c => ({ source: c.topic_id, target: c.id})))
      .concat(filteredSubtopics.map(st => ({ source: st.category_id, target: st.id})));

    console.log(links);

    setData({ nodes, links });
  });
}

const NaveTopicGraph = React.memo((_props) => {
  const [data, setData] = useState({
    nodes: [
      { id: 1, label: 'node1' },
      { id: 2, label: 'node2' },
      { id: 3, label: 'node3' },
      { id: 4, label: 'node4' },
    ],
    links: [
      { source: 1, target: 2 },
      { source: 1, target: 3 },
      { source: 1, target: 4 }
    ]
  })

  useEffect(() => {
    loadData(setData);
  }, [setData])

  const width = Math.min(window.innerWidth - 40, 760);

  return (
      <ForceGraph2D
        width={width}
        height={800}
        graphData={data}
        dagMode={null}
        dagLevelDistance={300}
        linkColor={() => 'rgba(0,0,0,0.2)'}
        nodeRelSize={1}
        nodeVal={n => n.reference_count / 8}
        nodeLabel="label"
        nodeAutoColorBy="reference_count"
        d3VelocityDecay={0.3} />
  );
  //{n => Math.sqrt(n.reference_count)}
  // linkDirectionalParticles={2}
  // linkDirectionalParticleWidth={2}
});

export default NaveTopicGraph;

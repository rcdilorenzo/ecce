import naveReference from '../data/nave-by-reference.json';
import naveTopics from '../data/nave-by-topic.json';
import * as R from 'ramda';
import { tsv } from 'd3-fetch';

export const topics = (book, chapter, verse) => {
  return Promise.resolve(naveReference[book][chapter][verse]);
};

export const allTopics = () => {
  return Promise.resolve(Object.keys(naveTopics));
};

export const topicNodes    = () => tsv('/data/nave-topic-nodes.tsv');
export const categoryNodes = () => tsv('/data/nave-category-nodes.tsv');
export const subtopicNodes = () => tsv('/data/nave-subtopic-nodes.tsv');

export const topicCounts = () => {
  const mapAsValues = f => R.pipe(Object.values, R.map(f))

  return Promise.resolve(R.map(R.pipe(
    mapAsValues(mapAsValues(mapAsValues(p => p.references.length))),
    R.flatten,
    R.sum
  ))(naveTopics));
};

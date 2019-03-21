import naveReference from '../data/nave-by-reference.json';
import naveTopics from '../data/nave-by-topic.json';
import * as R from 'ramda';

export const topics = (book, chapter, verse) => {
  return Promise.resolve(naveReference[book][chapter][verse]);
};

export const allTopics = () => {
  return Promise.resolve(Object.keys(naveTopics));
};

export const topicCounts = () => {
  const mapAsValues = f => R.pipe(Object.values, R.map(f))

  return Promise.resolve(R.map(R.pipe(
    mapAsValues(mapAsValues(mapAsValues(p => p.references.length))),
    R.flatten,
    R.sum
  ))(naveTopics));
};

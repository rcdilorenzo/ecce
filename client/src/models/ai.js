import * as R from 'ramda';
import * as Api from './api';
import * as Cluster from '../models/cluster';

const topicsLens = R.lensProp('topics');
const passageTopicsLens = R.lensProp('passage_topics');
const clustersLens = R.lensProp('clusters');

export const predict = R.pipe(
  Api.path.predict,
  Api.postJSON,
  R.then(R.pipe(
    R.over(topicsLens, Api.parseFrameJSON),
    R.over(clustersLens, R.pipe(Api.parseFrameJSON, R.map(Cluster.init), R.tap(console.log))),
    R.over(passageTopicsLens, Api.parseFrameJSON)
  ))
);

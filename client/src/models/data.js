import * as R from 'ramda';
import * as Api from './api';

const splitByComma = x => typeof(x) === 'string' ? x.split(',') : [];

export const byReference = R.pipe(
  Api.path.data.byReference,
  Api.fetchJSON,
  R.then(R.map(R.over(R.lensProp('topics'), splitByComma)))
);

export const topicStats = () => {
  return R.pipe(
    Api.fetchJSON,
    R.then(R.over(R.lensProp('counts'), Api.parseFrameJSON))
  )(Api.path.data.topicStats());
};

import * as R from 'ramda';
import * as Api from './api';

const memoize = R.memoizeWith(R.identity);
const splitByComma = x => typeof(x) === 'string' ? x.split(',') : [];

export const byReference = R.pipe(
  Api.path.data.byReference,
  Api.fetchJSON,
  R.then(R.map(R.over(R.lensProp('topics'), splitByComma)))
);

export const stats = memoize(() => {
  return Api.fetchJSON(Api.path.data.stats()).then(R.applySpec({
    topics: R.pipe(R.prop('topics'), Api.parseFrameJSON),
    verses: R.pipe(R.prop('verses'), Api.parseFrameJSON)
  }));
});

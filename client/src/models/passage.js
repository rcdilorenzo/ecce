import * as R from 'ramda';
import * as Api from './api';

const memoize = R.memoizeWith(R.identity);

export const defaultPassages = R.pipe(Api.path.passages.default, memoize(Api.fetchFrame));

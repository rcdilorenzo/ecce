import * as R from 'ramda';
import * as Api from './api';
import * as Reference from './reference';

export const init = ([name, references, text]) => ({
  name, references: references.map(Reference.init), text
});

const memoize = R.memoizeWith(R.identity);

export const defaultPassages = R.pipe(Api.path.passages.default, memoize(Api.fetchFrame));

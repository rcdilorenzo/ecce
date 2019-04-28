import * as R from 'ramda';
import * as Api from './api';
import * as Reference from './reference';

export const init = ([name, references, text]) => ({
  name, references: references.map(Reference.init), text
});

export const lines = ({ text }) => {
  const lines = text.split('\n');
  const previewLines = lines.slice(0, 3);
  return previewLines.concat(lines.length === previewLines.length ? [] : ['...']);
};

const memoize = R.memoizeWith(R.identity);

export const defaultPassages = R.pipe(Api.path.passages.default, memoize(Api.fetchFrame));

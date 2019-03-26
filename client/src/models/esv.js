import * as R from 'ramda';
import * as Api from './api';

import { CANONICAL_ORDER } from '../constants';

export const books = CANONICAL_ORDER;

export const references = () => Api.fetchJSON(Api.path.esv.references());

export const text = R.pipe(
  Api.path.esv.text,
  Api.fetchJSON,
  R.then(R.prop('text'))
);

export const verses = R.curry((referencesData, book, chapter) => {
  const verseCount = referencesData[book][chapter];
  return Array.from(Array(verseCount + 1).keys()).slice(1);
});

export const chapters = R.curry((referencesData, book) => {
  return Object.keys(referencesData[book]);
});

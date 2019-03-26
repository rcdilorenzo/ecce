import * as R from 'ramda';

import esv from '../data/ESV.json';
import { CANONICAL_ORDER } from '../constants';

export const books = CANONICAL_ORDER;

export const references = () => {
  return new Promise(resolve => {
    resolve(R.map(R.map(Object.keys), esv));
  });
};

export const text = (book, chapter, verse) => {
  return Promise.resolve(esv[book][chapter][verse]);
};

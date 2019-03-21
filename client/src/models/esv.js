import esv from '../data/ESV.json';
import { CANONICAL_ORDER } from '../constants';

export const books = CANONICAL_ORDER;

export const chapters = book => {
  return Promise.resolve(Object.keys(esv[book]));
};

export const verses = (book, chapter) => {
  return Promise.resolve(Object.keys(esv[book][chapter]));
};

export const text = (book, chapter, verse) => {
  return Promise.resolve(esv[book][chapter][verse]);
};

import naveReference from '../data/nave-by-reference.json';

export const topics = (book, chapter, verse) => {
  return Promise.resolve(naveReference[book][chapter][verse]);
};

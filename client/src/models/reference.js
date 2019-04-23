import * as Passage from './passage';

export const init = ([book, chapter, verse], text=null) => ({
  book, chapter, verse, text
});

export const toPassage = ({ book, chapter, verse, text=null }) => {
  return Passage.init([
    `${book} ${chapter}:${verse}`,
    [[book, chapter, verse]],
    text
 ]);
};

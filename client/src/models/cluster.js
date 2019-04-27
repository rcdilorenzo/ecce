import * as R from 'ramda';
import * as Passage from './passage';
import * as Reference from '../models/reference';

export const init = ({ probability, uuid, reference, text, passages }) => {
  return {
    probability,
    uuid,
    reference: Reference.init(reference, text),
    passages: R.map(Passage.init, passages)
  };
};

import * as R from 'ramda';
import * as Api from './api';
import * as Passage from '../models/passage';
import * as Reference from '../models/reference';

const clustersToTopLevelPassages = R.map(R.pipe(
  R.juxt([R.prop('reference'), R.prop('text')]),
  R.apply(Reference.init),
  Reference.toPassage,
));

const clustersToReferencedPassages = R.pipe(
  R.map(R.pipe(
    R.prop('passages'),
    R.map(Passage.init),
    R.tap(console.log)
  )),
  R.apply(R.concat)
);

const clustersToPassages = R.converge(R.concat, [
  clustersToTopLevelPassages,
  clustersToReferencedPassages
]);

export const predict = R.pipe(
  Api.path.predict,
  Api.postJSON,
  R.then(R.pipe(
    R.applySpec({
      topics: R.pipe(R.prop('topics'), Api.parseFrameJSON),
      passages: R.pipe(R.prop('clusters'), Api.parseFrameJSON, clustersToPassages)
    })
  )),
);

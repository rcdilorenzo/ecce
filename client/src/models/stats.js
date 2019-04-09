import * as R from 'ramda';
import { histogram } from 'd3-array';

const square = x => x ** 2;
const sqrt = Math.sqrt;
const PI = Math.PI;
const E = Math.E;
const isFractionalPercentage = x => Math.abs(x) <= 1;
const support = R.curry((when, f, u) => when(u) ? f(u) : 0);

export const kde = R.curry((kernel, bandwidth, values, x) => {
  const summation = R.sum(R.map(x_i => kernel((x - x_i) / bandwidth), values));
  const density = summation / (R.length(values) * bandwidth);
  return isNaN(density) ? 0 : density;
});

export const kernels = {
  epanechnikov: support(isFractionalPercentage, u => 0.75 * (1 - square(u))),
  gaussian: u => (1 / sqrt(2 * PI)) * (E ** (-0.5 * square(u)))
};

export const hist = histogram;

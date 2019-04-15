import * as R from 'ramda';
import * as Api from './api';

export const topics = R.pipe(Api.path.nave.reference, Api.fetchFrame);

export const topic = R.pipe(Api.path.nave.topic, Api.fetchJSON);

export const topicNodes = R.pipe(Api.path.nave.topics, Api.fetchFrame);

export const categoryNodes = R.pipe(Api.path.nave.categories, Api.fetchFrame);

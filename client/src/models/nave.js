import * as R from 'ramda';
import * as Api from './api';

export const topics = R.pipe(Api.path.nave.reference, Api.fetchFrame);

export const allTopics = R.pipe(Api.path.nave.topics, Api.fetchFrame);

export const topicNodes = () => Api.fetchFrame(Api.path.nave.topics());

export const categoryNodes = R.pipe(Api.path.nave.categories, Api.fetchFrame);

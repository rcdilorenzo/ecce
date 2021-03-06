import { zipObj } from 'ramda';
import qs from 'query-string';

export const parseFrameJSON = json => {
  return json.rows.map(zipObj(json.columns));
};

export const postJSON = path => {
  return fetch(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  }).then(r => r.json());
};

export const fetchJSON = (path, options = {}) => {
  return fetch(path, options).then(r => r.json());
};

export const fetchFrame = path => {
  return fetchJSON(path).then(parseFrameJSON);
};

export const path = {
  predict: (text) => (
    `/api/predict?${qs.stringify({ text })}`
  ),
  esv: {
    references: () => (
      '/api/esv/references'
    ),
    text: (book, chapter, verse) => (
      `/api/esv/text/${book}/${chapter}/${verse}`
    )
  },
  nave: {
    topic: (topicId, params={}) => (
      `/api/nave/topic/${topicId}?${qs.stringify(params)}`
    ),
    topics: (params={}) => (
      `/api/nave/topics?${qs.stringify(params)}`
    ),
    reference: (book, chapter, verse) => (
      `/api/nave/reference/${book}/${chapter}/${verse}`
    ),
    passages: (topicId) => (
      `/api/nave/topics/${topicId}/passages`
    ),
    categories: (topicId) => (
      `/api/nave/topics/${topicId}/categories`
    )
  },
  data: {
    stats: () => (
      '/api/data/stats'
    ),
    byReference: (book, chapter, verse) => (
      `/api/data/${book}/${chapter}/${verse}`
    )
  },
  passages: {
    default: (params={}) => (
      `/api/passages/default?${qs.stringify(params)}`
    )
  }
};

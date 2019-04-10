import React from 'react';
import TopicVerseHistogram from './TopicVerseHistogram';
import * as R from 'ramda';
import * as Data from '../../models/data';

const TopicCountByVerse = (props) => {
  const description = (minCount, counts, data) => (
    `Filtering verses with at least ${minCount} topics (${counts.length} of ${data.length} verses)`
  );

  return (
    <TopicVerseHistogram
      title="Topic Count by Verse"
      kdeMultiplier={20000}
      xAxisLabel="Topics per Verse"
      yAxisLabel="# Verses"
      bandwidth={0.6}
      sliderMarks={{ 1: 1, 4: 4, 8: 8, 12: 12 }}
      sliderMax={12}
      defaultMinCount={1}
      barWidth={10}
      binCount={30}
      promise={() => Data.stats().then(R.prop('topics'))}
      attr="topic_count"
      filterDescription={description} />
  );
};

export default React.memo(TopicCountByVerse);

import React from 'react';
import TopicVerseHistogram from './TopicVerseHistogram';
import * as R from 'ramda';
import * as Data from '../../models/data';

const VerseCountByTopic = (props) => {
  const description = (minCount, counts, data) => (
    `Filtering topics with at least ${minCount} verses (${counts.length} of ${data.length} topics)`
  );

  return (
    <TopicVerseHistogram
      title="Verse Count by Topic"
      kdeMultiplier={100000}
      xAxisLabel="Verses per Topic"
      yAxisLabel="# Topics"
      bandwidth={0.5}
      sliderMarks={{ 1: 1, 50: 50, 100: 100, 150: 150, 200: 200 }}
      sliderMax={200}
      defaultMinCount={30}
      barWidth={10}
      binCount={30}
      promise={() => Data.stats().then(R.prop('verses'))}
      attr="verse_count"
      filterDescription={description} />
  );
};

export default React.memo(VerseCountByTopic);

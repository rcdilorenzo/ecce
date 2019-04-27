import React from 'react';
import LoadingIndicator from 'react-loading-indicator';

import PassageBlock from '../PassageBlock';

const PassageResults = ({ data }) => (
  <React.Fragment>
      <h2>Passages</h2>
      {data.length === 0 && <p className="list-item">
        <LoadingIndicator />
        <span className="ml-2">Loading</span>
      </p>}
      {data.length > 0 && data.map(p =>
        <PassageBlock key={p.name} open={false} linkOnly={true} passage={p} />
      )}
    </React.Fragment>
  );

export default PassageResults;

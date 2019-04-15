import React from 'react';
import { Link } from 'react-router-dom';

const RealSearchResult = ({ id, label, reference_count, placeholder }) => (
  <Link to={`/topics/${id}`} className="no-underline text-black flex p-3 mb-1 border border-grey-darker hover:bg-grey-light">
    <header className="flex-grow">{label}</header>
    <p className="flex-no-grow align-right">{reference_count} Verses</p>
  </Link>
);

const PlaceholderSearchResult = _props => (
  <div>
    <header className="italic">Loading</header>
  </div>
);

const TopicSearchResult = (props) => {
  if (props.placeholder) {
    return <PlaceholderSearchResult {...props} />;
  } else {
    return <RealSearchResult {...props} />;
  }
 };

export default TopicSearchResult;
